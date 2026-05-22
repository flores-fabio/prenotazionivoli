import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Lemieprenotazioni } from './lemieprenotazioni';

describe('Lemieprenotazioni', () => {
  let component: Lemieprenotazioni;
  let fixture: ComponentFixture<Lemieprenotazioni>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Lemieprenotazioni],
    }).compileComponents();

    fixture = TestBed.createComponent(Lemieprenotazioni);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
