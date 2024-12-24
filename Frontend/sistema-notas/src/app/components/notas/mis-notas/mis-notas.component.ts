import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NotasService } from '../../../services/notas.service';
import { AuthService } from '../../../services/auth.service';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';

@Component({
  selector: 'app-mis-notas',
  standalone: true,
  imports: [CommonModule, NavbarComponent, NavbarComponent],
  templateUrl: './mis-notas.component.html',
  styleUrls: ['./mis-notas.component.css']
})
export class MisNotasComponent implements OnInit {
  notas: any[] = [];

  constructor(private notasService: NotasService, private authService: AuthService) {}

  ngOnInit(): void {
    const user = this.authService.getCurrentUser();
    if (user) {
      this.notasService.getNotas(user.id).subscribe({
        next: (res: any) => this.notas = res,
        error: (err) => console.error(err)
      });
    }
  }
}
