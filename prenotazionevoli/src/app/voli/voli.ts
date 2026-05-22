import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api';

@Component({
  selector: 'app-voli',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  templateUrl: './voli.html',
  styleUrl: './voli.css'
})
export class VoliComponent implements OnInit {

  compagnie: any[] = [];
  compagniaSelezionata: any = null;
  voli: any[] = [];
  voloSelezionato: any = null;
  filtri = { partenza: '', arrivo: '', data: '', compagnia: '' };
  vista: 'compagnie' | 'voli' | 'dettaglio' = 'compagnie';

  constructor(private api: ApiService, private route: ActivatedRoute, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.api.getCompagnie().subscribe({
      next: (data) => {
        this.compagnie = [...data];
        this.cdr.detectChanges();
      },
      error: (err) => console.log('Errore:', err)
    });
  }

  selezionaCompagnia(compagnia: any) {
    this.compagniaSelezionata = compagnia;
    this.filtri.compagnia = compagnia.id_compagnia;
    this.vista = 'voli';
    this.caricaVoli();
  }

  caricaVoli() {
    this.api.getVoli(this.filtri).subscribe({
      next: (data) => {
        this.voli = [...data];
        this.cdr.detectChanges();
      },
      error: (err) => console.log('Errore:', err)
    });
  }

  cercaVoli() {
    this.compagniaSelezionata = null;
    this.filtri.compagnia = '';
    this.vista = 'voli';
    this.caricaVoli();
  }

  selezionaVolo(volo: any) {
    this.api.getVolo(volo.id_volo).subscribe({
      next: (data) => {
        this.voloSelezionato = data;
        this.vista = 'dettaglio';
        this.cdr.detectChanges();
      },
      error: (err) => console.log('Errore:', err)
    });
  }

  tornaACompagnie() {
    this.vista = 'compagnie';
    this.compagniaSelezionata = null;
    this.voloSelezionato = null;
    this.filtri = { partenza: '', arrivo: '', data: '', compagnia: '' };
    this.cdr.detectChanges();
  }

  tornaAVoli() {
    this.vista = 'voli';
    this.voloSelezionato = null;
    this.cdr.detectChanges();
  }
}