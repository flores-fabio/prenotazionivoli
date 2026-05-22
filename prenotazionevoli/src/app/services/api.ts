import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'https://urban-space-rotary-phone-g47jjwpvq5jx295j4-5000.app.github.dev/api';

  constructor(private http: HttpClient) {}

  getCompagnie(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/compagnie`);
  }

  getCompagnia(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/compagnie/${id}`);
  }

  getVoli(filtri?: any): Observable<any[]> {
    let params = '';
    if (filtri) {
      const query = Object.keys(filtri)
        .filter(k => filtri[k])
        .map(k => `${k}=${filtri[k]}`)
        .join('&');
      if (query) params = '?' + query;
    }
    return this.http.get<any[]>(`${this.apiUrl}/voli${params}`);
  }

  getVolo(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/voli/${id}`);
  }

  getPrenotazioni(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/prenotazioni`);
  }

  creaPrenotazione(data: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/prenotazioni`, data);
  }

  getUtenti(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/utenti`);
  }
}