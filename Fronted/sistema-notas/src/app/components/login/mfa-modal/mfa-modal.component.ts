import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-mfa-modal',
  standalone: true,
  imports: [CommonModule, FormsModule, MatInputModule, MatButtonModule],
  templateUrl: './mfa-modal.component.html',
  styleUrls: ['./mfa-modal.component.css']
})
export class MfaModalComponent {
  @Input() usuarioId: number | null = null;
  @Output() verificado = new EventEmitter<boolean>();
  @Output() cerrar = new EventEmitter<void>();

  codigoMFA = '';
  mensajeError = '';

  constructor(private authService: AuthService) {}

  verificar() {
    if (this.usuarioId == null) {
      this.mensajeError = 'No se recibió usuarioId válido';
      this.verificado.emit(false);
      return;
    }

    this.authService.verificarCodigoMFA(this.usuarioId, this.codigoMFA).subscribe({
      next: () => {
        // Código correcto => emitimos "true" para notificar éxito
        this.verificado.emit(true);
      },
      error: (err) => {
        // Si el backend lanza 401 u otro error, lo manejamos aquí
        this.mensajeError = err.error?.error || 'Código incorrecto';
        this.verificado.emit(false);
      }
    });
  }
}
