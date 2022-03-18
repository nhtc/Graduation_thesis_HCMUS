import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';

import { AboutRoutingModule } from './about-routing.module';
import { AboutComponent } from './about.component';
import { SharedModule } from '../shared/shared.module';

@NgModule({
  imports: [CommonModule, TranslateModule, AboutRoutingModule, SharedModule],
  declarations: [AboutComponent],
})
export class AboutModule {}
