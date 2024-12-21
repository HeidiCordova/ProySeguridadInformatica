import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { AuthService } from '../../services/auth.service';
import { MfaModalComponent } from './mfa-modal/mfa-modal.component';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MfaModalComponent
  ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email = '';
  clave = '';
  mensajeError = '';
  intentosRestantes: number | null = null;
  bloqueado = false;

  // Control de MFA
  mostrarMfaModal = false;
  mostrarMfaPregunta = false;

  usuarioId: number | null = null;
  rol: string | null = null;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  login() {
    if (!this.email || !this.clave) {
      this.mensajeError = 'Correo y clave son requeridos';
      return;
    }

    if (this.bloqueado) {
      this.mensajeError = 'Usuario bloqueado temporalmente. Inténtalo más tarde.';
      return;
    }

    this.authService.login(this.email, this.clave).subscribe({
      next: (response: any) => {
        // El backend puede devolver:
        // - mfa_required = true (usuario ya tiene MFA)
        // - mfa_can_enable = true (puede habilitar)
        // - De lo contrario, login normal
        this.usuarioId = response.usuario_id;
        this.rol = response.rol;

        if (response.mfa_required) {
          // Pedimos el modal MFA
          this.mostrarMfaModal = true;
        } else if (response.mfa_can_enable) {
          // Ofrecemos habilitar MFA
          this.mostrarMfaPregunta = true;
        } else {
          // Login normal (sin MFA ni oferta)
          this.finalizarLogin(this.rol!);
        }
      },
      error: (err) => this.manejarErrorLogin(err)
    });
  }

  // Cuando el modal de MFA termine la verificación
  onMfaVerificado(exito: boolean) {
    if (exito) {
      // MFA correcta => cerrar el modal y finalizar
      this.mostrarMfaModal = false;
      this.finalizarLogin(this.rol!);
    } else {
      // MFA incorrecta => el modal muestra error, no navega
    }
  }

  // Preguntar si el usuario quiere habilitar MFA
  activarMFA() {
    if (!this.usuarioId) return;
    this.authService.habilitarMFA(this.usuarioId).subscribe({
      next: () => {
        // Asumiendo que se generó el QR, etc. 
        // Podrías mostrar un mensaje o redirigir. 
        alert('MFA habilitada. Configura tu autenticador.');
        this.finalizarLogin(this.rol!);
      },
      error: (err) => {
        this.mensajeError = err.error?.error || 'Error al habilitar MFA';
      }
    });
  }

  rechazarMFA() {
    this.finalizarLogin(this.rol!);
  }

  finalizarLogin(rol: string) {
    this.authService.setCurrentUser({ email: this.email, rol, id: this.usuarioId });
    if (rol === 'admin') {
      this.router.navigate(['/dashboard-admin']);
    } else if (rol === 'profesor') {
      this.router.navigate(['/dashboard-profesor']);
    } else {
      // Se asume 'estudiante' o cualquier otro
      this.router.navigate(['/dashboard-estudiante']);
    }
  }

  manejarErrorLogin(err: any) {
    this.mensajeError = err.error?.error || 'Error desconocido';
    if (this.mensajeError.includes('bloqueado')) {
      this.bloqueado = true;
    }
    const match = this.mensajeError.match(/(\d+) intentos/);
    if (match) {
      this.intentosRestantes = parseInt(match[1], 10);
    }
  }
}
