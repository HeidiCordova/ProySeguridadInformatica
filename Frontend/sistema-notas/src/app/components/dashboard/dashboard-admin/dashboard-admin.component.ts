import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../services/auth.service';
import { Router } from '@angular/router';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';

@Component({
  selector: 'app-dashboard-admin',
  standalone: true,
  imports: [CommonModule, NavbarComponent],
  templateUrl: './dashboard-admin.component.html',
  styleUrls: ['./dashboard-admin.component.css']
})
export class DashboardAdminComponent {
  
  // Aquí muestras vista específica para admin
  usuarios: any[] = []; // Aquí se almacenará la lista de usuarios
  mostrarUsuarios: boolean = false; // Controlará si mostramos la tabla de usuarios
  
  usuarioId: number | null = null;
  rol: string | null = null;
  
  constructor(
      private authService: AuthService,
      private router: Router
    ) {}
  

  // Método para cargar usuarios
  cargarUsuarios(): void {
    this.authService.getUsuarios().subscribe(
      (data) => {
        this.usuarios = data; // Guardamos los usuarios en la variable
        this.mostrarUsuarios = true; // Mostramos la tabla
      },
      (error) => {
        console.error('Error al cargar los usuarios:', error);
      }
    );
  }
}
