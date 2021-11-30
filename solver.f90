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
	real(kind=kind_real) :: h2, ecart, ecart_min
	integer :: i = 0, j = 0

	h2 = h**2

	ecart = 1

	ecart_min = delta_convgce**2

	do while (ecart > ecart_min)
		phi0 = phi
  		do i=2, qi-1
			do j=2, qj-1
			phi(i, j) = 0.25*(h2*w(i, j) + phi(i-1, j) +phi(i+1, j) + phi(i ,j-1) + phi(i ,j+1))
   			end do
   		end do
		ecart = maxval((phi0 - phi)**2)
		if (i > 100000) then
			erreur = 1
			ecart = 0
		end if
	end do
end subroutine poisson
!****************************************************************************

subroutine jellyfish(w, phi, tmax, dt, h, delta_convgce, nu, u_top_wall, u_bot_wall, qi, qj, erreur)
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
	
	real(kind=kind_real), dimension(qi-2,qj-2) :: advec, diffusion
	
	real(kind=kind_real) :: nu_h2, h_2, h2
	
	integer :: n_it,i
	erreur = 0
	i = 1
	h2 = h**2
	h_2 = 2.0*h
	nu_h2 = nu/(h**2)
	n_it = ceiling(tmax/dt) 
	
	do i = 1, n_it, 1
		call poisson(w,phi,qi,qj,h,delta_convgce, erreur)
		w(2:qi-1,1) = -phi(2:qi-1,2)*2.0/h2     !mur gauche
		w(2:qi-1,qj) = -phi(2:qi-1,qj-1)*2.0/h2		!mur droite
		w(1,2:qj-1) = -phi(2,2:qj-1)*2.0/h2 + u_bot_wall*2.0/h		!mur bas
		w(qi,2:qj-1) = -phi(qi-1,2:qj-1)*2.0/h2 - u_top_wall*2.0/h	!mur haut
		
		diffusion = (w(3:qi,2:qj-1)+w(1:qi-2,2:qj-1)+w(2:qi-1,3:qj)+ &
			& w(2:qi-1,1:qj-2)-4*w(2:qi-1,2:qj-1))*nu_h2
		
		advec = ((phi(2:qi-1,3:qj)-phi(2:qi-1,1:qj-2))*(w(3:qi,2:qj-1)-w(1:qi-2,2:qj-1)) &
			& - (w(2:qi-1,3:qj)-w(2:qi-1,1:qj-2))*(phi(3:qi,2:qj-1)-phi(1:qi-2,2:qj-1)))/h_2

		w(2:qi-1,2:qj-1) = w(2:qi-1,2:qj-1) + dt*(advec + diffusion)

	end do
end subroutine jellyfish



