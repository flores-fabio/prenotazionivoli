import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Voli } from './voli';

describe('Voli', () => {
  let component: Voli;
  let fixture: ComponentFixture<Voli>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Voli],
    }).compileComponents();

    fixture = TestBed.createComponent(Voli);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
