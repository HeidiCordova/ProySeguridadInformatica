import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MisNotasComponent } from './mis-notas.component';

describe('MisNotasComponent', () => {
  let component: MisNotasComponent;
  let fixture: ComponentFixture<MisNotasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MisNotasComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MisNotasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
