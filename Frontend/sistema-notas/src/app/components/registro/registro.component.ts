import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { AuthService } from '../../services/auth.service';
import { NavbarComponent } from '../../shared/navbar/navbar.component';

@Component({
  selector: 'app-registro',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule,
    MatSelectModule, 
    NavbarComponent
  ],
  templateUrl: './registro.component.html',
  styleUrls: ['./registro.component.css']
})
export class RegistroComponent {
  // Campos del formulario
  nombre = '';
  email = '';
  clave = '';
  rol = '';

  // Control de errores y mensajería
  mensajeError = '';

  // Control de MFA
  mostrarMfaPregunta = false;
  qrUrl: string | null = null;
  qrImageBase64: string | null = null;

  // Guardamos ID del usuario tras registro, para habilitar MFA
  usuarioId: number | null = null;
  logueado = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  // Al enviar el formulario de registro
  onRegister() {
    if (!this.nombre || !this.email || !this.clave || !this.rol) {
      this.mensajeError = 'Todos los campos son requeridos.';
      return;
    }

    this.authService.register(this.nombre, this.email, this.clave, this.rol).subscribe({
      next: (res: any) => {
        // Respuesta exitosa: {id, message}
        this.usuarioId = res.id;
        // Tras registrarse, preguntamos si desea habilitar MFA
        this.mostrarMfaPregunta = true;
      },
      error: (err) => {
        this.mensajeError = err.error?.error || 'Error en el registro';
      }
    });
  }

  // Si el usuario decide habilitar MFA
  habilitarMFA() {
    if (!this.usuarioId) return;

    this.authService.habilitarMFA(this.usuarioId).subscribe({
      next: (res: any) => {
        // Esperamos { message, qr_url, qr_image_base64 }
        this.qrUrl = res.qr_url;
        this.qrImageBase64 = res.qr_image_base64;
        this.mostrarMfaPregunta = false;
        this.logueado = true;
      },
      error: (err) => {
        this.mensajeError = err.error?.error || 'Error al habilitar MFA';
      }
    });
  }

  // Si el usuario NO quiere habilitar MFA
  noHabilitarMFA() {
    // Redirigir al login para que use el nuevo usuario
    this.router.navigate(['/login']);
  }

  continuar() {
    // Redirigir al login para que use el nuevo usuario
    this.ingresarSegunRol(this.rol!);
  }
  
  ingresarSegunRol(rol: string) {
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

  recargarPagina() {
    window.location.reload(); // Recarga la página actual
  }
}
