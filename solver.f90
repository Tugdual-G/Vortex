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
	
	real(kind=kind_real) :: h2, ecart_min, r_sum=0, ih2
	integer :: i = 0, j = 0, k=0

	h2 = h**2
 	ih2 = 1/h2

	ecart_min = delta_convgce*qi*qj
 	r_sum = ecart_min + 1

	do while (r_sum > ecart_min)
  		r_sum = 0
		do k=0, 5
			do j=2, qj-1
				do i=2, qi-1
					phi(i, j) = 0.25*(h2*w(i, j) + phi(i-1, j) +phi(i+1, j) + phi(i ,j-1) + phi(i ,j+1))
				end do
			end do
	 	end do
		do j=2, qj-1
			do i=2, qi-1
				phi(i, j) = 0.25*(h2*w(i, j) + phi(i-1, j) +phi(i+1, j) + phi(i ,j-1) + phi(i ,j+1))
				r_sum += ABS(w(i,j)+(phi(i-1, j) + phi(i+1, j) + phi(i ,j-1) + phi(i ,j+1) - 4*phi(i, j))*ih2)
			end do
		end do
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

	real(kind=kind_real), dimension(qi-2,qj-2) :: advec, diffusion
	
	real(kind=kind_real) :: nu_h2, h_2, h2
	
	integer :: n_it,i
	erreur = 0
	i = 1
	h2 = h**2
	h_2 = 2.0*h
	nu_h2 = nu/(h**2)
	n_it = ceiling(tmax/dt) 

	if (no_slip) then
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
	else
		do i = 1, n_it, 1
			call poisson(w,phi,qi,qj,h,delta_convgce, erreur)

			diffusion = (w(3:qi,2:qj-1)+w(1:qi-2,2:qj-1)+w(2:qi-1,3:qj)+ &
				& w(2:qi-1,1:qj-2)-4*w(2:qi-1,2:qj-1))*nu_h2

			advec = ((phi(2:qi-1,3:qj)-phi(2:qi-1,1:qj-2))*(w(3:qi,2:qj-1)-w(1:qi-2,2:qj-1)) &
				& - (w(2:qi-1,3:qj)-w(2:qi-1,1:qj-2))*(phi(3:qi,2:qj-1)-phi(1:qi-2,2:qj-1)))/h_2

			w(2:qi-1,2:qj-1) = w(2:qi-1,2:qj-1) + dt*(advec + diffusion)

		end do
    end if
end subroutine jellyfish



