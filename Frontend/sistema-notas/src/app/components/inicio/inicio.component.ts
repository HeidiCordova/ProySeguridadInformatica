import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { NavbarComponent } from '../../shared/navbar/navbar.component';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule, MatButtonModule, NavbarComponent],
  templateUrl: './inicio.component.html',
  styleUrls: ['./inicio.component.css']
})
export class InicioComponent {
  constructor(private router: Router){}

  irALogin() { this.router.navigate(['/login']); }
  irARegistro() { this.router.navigate(['/register']); }
}
