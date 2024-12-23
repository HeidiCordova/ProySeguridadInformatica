import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../services/auth.service';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';

@Component({
  selector: 'app-dashboard-profesor',
  standalone: true,
  imports: [CommonModule, FormsModule, NavbarComponent],
  templateUrl: './dashboard-profesor.component.html',
  styleUrls: ['./dashboard-profesor.component.css']
})
export class DashboardProfesorComponent {
  
  estudiantes: any[] = []; // Aquí se almacenará la lista de estudiantes
  mostrarEstudiantes: boolean = false; // Controlará si mostramos la tabla de estudiantes
  
  nombreEstudiante: string = ''; // Nombre del estudiante para asignar nota
  notaContenido: string = ''; // Contenido de la nota
  asignacionExitosa: string = ''; // Mensaje de éxito
  asignacionError: string = ''; // Mensaje de error

  constructor(private authService: AuthService) {}

  // Método para cargar estudiantes
  cargarEstudiantes(): void {
    this.authService.getEstudiantes().subscribe(
      (data) => {
        this.estudiantes = data; // Guardamos los estudiantes en la variable
        this.mostrarEstudiantes = true; // Mostramos la tabla
      },
      (error) => {
        console.error('Error al cargar los estudiantes:', error);
      }
    );
  }

  // Asignar nota
  asignarNota(): void {
    if (!this.nombreEstudiante.trim() || !this.notaContenido.trim()) {
      this.asignacionError = 'El nombre del estudiante y la nota son requeridos.';
      return;
    }

    this.authService.asignarNota(this.nombreEstudiante, this.notaContenido).subscribe(
      (response) => {
        this.asignacionExitosa = `Nota asignada a ${this.nombreEstudiante} exitosamente.`;
        this.asignacionError = '';
        this.nombreEstudiante = ''; // Limpiar campos
        this.notaContenido = '';
      },
      (error) => {
        this.asignacionError = `Error al asignar la nota: ${error.error?.message || 'Error desconocido'}`;
        this.asignacionExitosa = '';
      }
    );
  }
}
