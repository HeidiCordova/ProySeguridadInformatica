import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';

@Injectable({providedIn: 'root'})
export class AuthService {
  private baseUrl = 'http://localhost:5000/api'; // Ajusta al backend
  private currentUserSubject = new BehaviorSubject<any>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {}

  register(nombre: string, email: string, clave: string, rol: string) {
    return this.http.post(`${this.baseUrl}/register`, {nombre, email, clave, rol});
  }

  login(email: string, clave: string) {
    return this.http.post(`${this.baseUrl}/login`, {email, clave});
  }

  verificarCodigoMFA(usuario_id: number, codigo_mfa: string) {
    return this.http.post(`${this.baseUrl}/verificarCodigoMFA`, {usuario_id, codigo_mfa});
  }

  habilitarMFA(usuario_id: number) {
    return this.http.post(`${this.baseUrl}/habilitarMFA`, {usuario_id});
  }

  setCurrentUser(user: any) {
    this.currentUserSubject.next(user);
  }

  getCurrentUser() {
    return this.currentUserSubject.value;
  }
}
