import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({providedIn: 'root'})
export class NotasService {
  private baseUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  getNotas(usuario_id: number) {
    return this.http.get(`${this.baseUrl}/notas?usuario_id=${usuario_id}`);
  }
}
