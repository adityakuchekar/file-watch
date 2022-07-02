import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EventServiceService {
  config: any;
  fileList: any = [];

  constructor(private http: HttpClient) {
    this.config = {
      filePathUrl: "http://127.0.0.1:5000/file-list",
      closeConenctionUrl: "http://127.0.0.1:5000/close"
    }
  }

  getFiles(): Observable<any> {
    const url = this.config.filePathUrl;
    return this.http.get(url);
  }

  closeConnection(): Observable<any> {
    const url = this.config.closeConenctionUrl;
    return this.http.get(url);
  }

}
