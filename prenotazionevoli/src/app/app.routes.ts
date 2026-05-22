import { Routes } from '@angular/router';
import { HomeComponent } from './home/home';
import { VoliComponent } from './voli/voli';
import { Lemieprenotazioni } from './lemieprenotazioni/lemieprenotazioni';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'voli', component: VoliComponent },
  { path: 'lemieprenotazioni', component: Lemieprenotazioni },
  { path: '**', redirectTo: '' }
];