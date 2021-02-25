subroutine poisson(w,phi,qi,qj,h,delta_convgce, erreur)
	implicit none
	
	integer, parameter :: kind_real = SELECTED_REAL_KIND(p=15,r=6)
	
	integer, intent(in) :: qi, qj
!f2py intent(in) :: qi,qj
	
	integer, intent(inout) :: erreur
	
	real(kind=kind_real), intent(inout), dimension(qi,qj) :: phi
!f2py intent(in,out) :: phi
    	
	real(kind=kind_real), intent(in), dimension(qi,qj) :: w
!f2py intent(in) :: w
	
	
	real(kind=kind_real), intent(in) :: delta_convgce, h
!f2py intent(in) :: delta_convgce, h
	
	real(kind=kind_real), dimension(qi,qj) :: phi0
	real(kind=kind_real) :: h2, ecart, ecart_max
	integer :: i = 0	
	integer, dimension(floor((qj-2.0)/2.0)) :: list_j 	
	
	list_j = [ (i, i=3, qj ,2) ]
	
	h2 = h**2
	
	ecart = 1
	
	ecart_max = delta_convgce**2
	
	do while (ecart > ecart_max)
		i = i+1
		phi0 = phi
		
	 	phi(2:qi-1:2, 2:qj-1:2) = 0.25*(h2*w(2:qi-1:2, 2:qj-1:2) &
	 	& + phi(1:qi-2:2, 2:qj-1:2) + &
	 		& phi(3:qi:2,2:qj-1:2) + phi(2:qi-1:2,1:qj-2:2) + phi(2:qi-1:2,3:qj:2))
	 	
	 	phi(3:qi-1:2, 3:qj-1:2) = 0.25*(h2*w(3:qi-1:2, 3:qj-1:2) &
	 	& + phi(2:qi-2:2, 3:qj-1:2) + &
	 		& phi(4:qi:2, 3:qj-1:2) + phi(3:qi-1:2, 2:qj-2:2) + phi(3:qi-1:2, 4:qj:2))
	 	
	 	phi(3:qi-1:2, 2:qj-1:2) = 0.25*(h2*w(3:qi-1:2, 2:qj-1:2) &
	 	& + phi(2:qi-2:2, 2:qj-1:2) + &
	 		& phi(4:qi:2,2:qj-1:2) + phi(3:qi-1:2,1:qj-2:2) + phi(3:qi-1:2,3:qj:2))
	 	
	 	phi(4:qi-1:2, 3:qj-1:2) = 0.25*(h2*w(4:qi-1:2, 3:qj-1:2) &
	 	& + phi(3:qi-2:2, 3:qj-1:2) + &
	 		& phi(5:qi:2, 3:qj-1:2) + phi(4:qi-1:2, 2:qj-2:2) + phi(4:qi-1:2, 4:qj:2))
		
		phi(2, list_j) = 0.25*(h2*w(2, list_j) + phi(1, list_j) + phi(3, list_j) + &
			& phi(2, list_j-1) + phi(2, list_j+1))
			
		ecart = maxval((phi0 - phi)**2)
		if (i > 10000000) then
			erreur = 1
			ecart = 0 
		end if
	end do			
end subroutine poisson

!****************************************************************************

subroutine jellyfish(w, phi, tmax, dt, h, delta_convgce, nu, u_top_wall, u_bot_wall, qi, qj, erreur, no_slip)
	implicit none
	integer, parameter :: kind_real = SELECTED_REAL_KIND(p=15,r=6)

	real(kind=kind_real), intent(inout), dimension(qi,qj) :: phi, w
!f2py intent(in,out) :: w, phi
	
	integer, intent(inout) :: erreur
!f2py intent(in,out) :: erreur   	
	
	real(kind=kind_real), intent(in) :: tmax, dt, h, delta_convgce, nu, u_top_wall, u_bot_wall
!f2py intent(in) :: tmax, dt, h, delta_convgce, nu, u_top_wall, u_bot_wall
	
	integer, intent(in) :: qi, qj
!f2py intent(in) :: qi, qj	
	
	logical, intent(in) :: no_slip
!f2py intent(in) :: no_slip
	
	real(kind=kind_real), dimension(qi,qj) :: w_k, k0, k1, k2, k3
	
	real(kind=kind_real), dimension(qi-2,qj-2) :: advec, diffusion
	
	real(kind=kind_real) :: nu_h2, h_2, h2
		
	
	integer :: n_it,i
	erreur = 0
	i = 1
	h2 = h**2
	h_2 = 2.0*h
	nu_h2 = nu/(h**2)
	n_it = ceiling(tmax/dt) 
	k0(1:qi,1:qj) = 0
	k1(1:qi,1:qj) = 0
	k2(1:qi,1:qj) = 0
	k3(1:qi,1:qj) = 0
	
	do i = 1, n_it, 1
		call poisson(w,phi,qi,qj,h,delta_convgce, erreur)
		if (no_slip) then
			w(2:qi-1,1) = -phi(2:qi-1,2)*2.0/h2     !mur gauche
			w(2:qi-1,qj) = -phi(2:qi-1,qj-1)*2.0/h2		!mur droite
			w(1,2:qj-1) = -phi(2,2:qj-1)*2.0/h2 + u_bot_wall*2.0/h		!mur bas
			w(qi,2:qj-1) = -phi(qi-1,2:qj-1)*2.0/h2 - u_top_wall*2.0/h	!mur haut
		end if
		diffusion = (w(3:qi,2:qj-1)+w(1:qi-2,2:qj-1)+w(2:qi-1,3:qj)+ &
			& w(2:qi-1,1:qj-2)-4*w(2:qi-1,2:qj-1))*nu_h2
		
		advec = ((phi(2:qi-1,3:qj)-phi(2:qi-1,1:qj-2))*(w(3:qi,2:qj-1)-w(1:qi-2,2:qj-1)) &
			& - (w(2:qi-1,3:qj)-w(2:qi-1,1:qj-2))*(phi(3:qi,2:qj-1)-phi(1:qi-2,2:qj-1)))/h_2		
		k0(2:qi-1,2:qj-1) = dt*(advec + diffusion)
		
!******** Second point Runge Kutta 4	
		w_k = w + k0/2.0		
		call poisson(w_k,phi,qi,qj,h,delta_convgce, erreur)
		if (no_slip) then
			w_k(2:qi-1,1) = -phi(2:qi-1,2)*2.0/h2     !mur gauche
			w_k(2:qi-1,qj) = -phi(2:qi-1,qj-1)*2.0/h2		!mur droite
			w_k(1,2:qj-1) = -phi(2,2:qj-1)*2.0/h2 + u_bot_wall*2.0/h		!mur bas
			w_k(qi,2:qj-1) = -phi(qi-1,2:qj-1)*2.0/h2 - u_top_wall*2.0/h	!mur haut
		end if		
		diffusion = (w_k(3:qi,2:qj-1)+w_k(1:qi-2,2:qj-1)+w_k(2:qi-1,3:qj)+ &
			& w_k(2:qi-1,1:qj-2)-4*w_k(2:qi-1,2:qj-1))*nu_h2
		
		advec = ((phi(2:qi-1,3:qj)-phi(2:qi-1,1:qj-2))*(w_k(3:qi,2:qj-1)-w_k(1:qi-2,2:qj-1)) &
			& - (w_k(2:qi-1,3:qj)-w_k(2:qi-1,1:qj-2))*(phi(3:qi,2:qj-1)-phi(1:qi-2,2:qj-1)))/h_2		
		k1(2:qi-1,2:qj-1) = dt*(advec + diffusion)

!******** Troisieme point Runge Kutta 4			
		w_k = w + k1/2.0
		call poisson(w_k,phi,qi,qj,h,delta_convgce, erreur)
		if (no_slip) then
			w_k(2:qi-1,1) = -phi(2:qi-1,2)*2.0/h2     !mur gauche
			w_k(2:qi-1,qj) = -phi(2:qi-1,qj-1)*2.0/h2		!mur droite
			w_k(1,2:qj-1) = -phi(2,2:qj-1)*2.0/h2 + u_bot_wall*2.0/h		!mur bas
			w_k(qi,2:qj-1) = -phi(qi-1,2:qj-1)*2.0/h2 - u_top_wall*2.0/h	!mur haut
		end if				
		diffusion = (w_k(3:qi,2:qj-1)+w_k(1:qi-2,2:qj-1)+w_k(2:qi-1,3:qj)+ &
			& w_k(2:qi-1,1:qj-2)-4*w_k(2:qi-1,2:qj-1))*nu_h2
		
		advec = ((phi(2:qi-1,3:qj)-phi(2:qi-1,1:qj-2))*(w_k(3:qi,2:qj-1)-w_k(1:qi-2,2:qj-1)) &
			& - (w_k(2:qi-1,3:qj)-w_k(2:qi-1,1:qj-2))*(phi(3:qi,2:qj-1)-phi(1:qi-2,2:qj-1)))/h_2		
		k2(2:qi-1,2:qj-1) = dt*(advec + diffusion)

!******** Quatrieme point Runge Kutta 4	
		w_k = w + k2
		call poisson(w_k,phi,qi,qj,h,delta_convgce, erreur)
		if (no_slip) then
			w_k(2:qi-1,1) = -phi(2:qi-1,2)*2.0/h2     !mur gauche
			w_k(2:qi-1,qj) = -phi(2:qi-1,qj-1)*2.0/h2		!mur droite
			w_k(1,2:qj-1) = -phi(2,2:qj-1)*2.0/h2 + u_bot_wall*2.0/h		!mur bas
			w_k(qi,2:qj-1) = -phi(qi-1,2:qj-1)*2.0/h2 - u_top_wall*2.0/h	!mur haut
		end if		
		diffusion = (w_k(3:qi,2:qj-1)+w_k(1:qi-2,2:qj-1)+w_k(2:qi-1,3:qj)+ &
			& w_k(2:qi-1,1:qj-2)-4*w_k(2:qi-1,2:qj-1))*nu_h2
		
		advec = ((phi(2:qi-1,3:qj)-phi(2:qi-1,1:qj-2))*(w_k(3:qi,2:qj-1)-w_k(1:qi-2,2:qj-1)) &
			& - (w_k(2:qi-1,3:qj)-w_k(2:qi-1,1:qj-2))*(phi(3:qi,2:qj-1)-phi(1:qi-2,2:qj-1)))/h_2		
		k3(2:qi-1,2:qj-1) = dt*(advec + diffusion)

!******** Reunion et moyenne ponderee des approximations, calcul de n+1			
		w(2:qi-1,2:qj-1) = w(2:qi-1,2:qj-1) + (k0(2:qi-1,2:qj-1)+2*k1(2:qi-1,2:qj-1)+2*k2(2:qi-1,2:qj-1)+k3(2:qi-1,2:qj-1))/6

	end do
end subroutine jellyfish

