import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api';

@Component({
  selector: 'app-lemieprenotazioni',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './lemieprenotazioni.html',
  styleUrl: './lemieprenotazioni.css'
})
export class Lemieprenotazioni implements OnInit {

  prenotazioni: any[] = [];
  utenti: any[] = [];
  voli: any[] = [];
  nuovaPrenotazione = { id_utente: '', id_volo: '' };
  messaggio = '';
  errore = '';

  constructor(private api: ApiService, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.caricaPrenotazioni();
    this.api.getUtenti().subscribe({
      next: (data) => { this.utenti = [...data]; this.cdr.detectChanges(); }
    });
    this.api.getVoli().subscribe({
      next: (data) => { this.voli = [...data]; this.cdr.detectChanges(); }
    });
  }

  caricaPrenotazioni() {
    this.api.getPrenotazioni().subscribe({
      next: (data) => { this.prenotazioni = [...data]; this.cdr.detectChanges(); }
    });
  }

  creaPrenotazione() {
    this.messaggio = '';
    this.errore = '';
    if (!this.nuovaPrenotazione.id_utente || !this.nuovaPrenotazione.id_volo) {
      this.errore = 'Seleziona un utente e un volo!';
      this.cdr.detectChanges();
      return;
    }
    this.api.creaPrenotazione(this.nuovaPrenotazione).subscribe({
      next: () => {
        this.messaggio = '✅ Prenotazione creata con successo!';
        this.nuovaPrenotazione = { id_utente: '', id_volo: '' };
        this.caricaPrenotazioni();
        this.cdr.detectChanges();
      },
      error: () => {
        this.errore = '❌ Errore nella creazione della prenotazione.';
        this.cdr.detectChanges();
      }
    });
  }
}