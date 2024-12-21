import { Routes } from '@angular/router';
import { InicioComponent } from './components/inicio/inicio.component';
import { LoginComponent } from './components/login/login.component';
import { RegistroComponent } from './components/registro/registro.component';
import { DashboardAdminComponent } from './components/dashboard/dashboard-admin/dashboard-admin.component';
import { DashboardProfesorComponent } from './components/dashboard/dashboard-profesor/dashboard-profesor.component';
import { DashboardEstudianteComponent } from './components/dashboard/dashboard-estudiante/dashboard-estudiante.component';
import { MisNotasComponent } from './components/notas/mis-notas/mis-notas.component';

export const routes: Routes = [
  { path: '', component: InicioComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegistroComponent },
  { path: 'dashboard-admin', component: DashboardAdminComponent },
  { path: 'dashboard-profesor', component: DashboardProfesorComponent },
  { path: 'dashboard-estudiante', component: DashboardEstudianteComponent },
  { path: 'mis-notas', component: MisNotasComponent },
  { path: '**', redirectTo: '' }
];
