import { Component, OnInit } from '@angular/core';
import { EventServiceService } from '../services/event-service.service'
@Component({
  selector: 'app-file-list',
  templateUrl: './file-list.component.html',
  styleUrls: ['./file-list.component.scss']
})
export class FileListComponent implements OnInit {

  directoryPath = "";
  myData: any;
  config: any;
  fileList: any = [];
  changeLog: any = [];
  watchFlag = true;
  stopFlag = false;
  constructor(private eventService: EventServiceService) {
    this.config = {
      eventStreamUrl: "http://127.0.0.1:5000/events"
    }
  }

  ngOnInit(): void {    
    //this call makes sure that after refresh / first load, any previous connection is closed
    this.eventService.closeConnection().subscribe(data => {
      console.log("Oninit connection close")
    });
  }

  startWatching() {
    this.fileList = this.eventService.getFiles().subscribe(data => {
      data.sort()
      this.fileList = data;      
      this.connect();
      this.watchFlag = !this.watchFlag;
      this.stopFlag = !this.stopFlag;
    });

  }

  connect(): void {
    let source = new EventSource(this.config.eventStreamUrl);

    source.addEventListener('message', message => {
      let messageData = JSON.parse(message.data);      
      this.handleFileEvent(messageData, source);
    });
  }

  handleFileEvent(event: any, source: EventSource) {    
    if (event.event_type === "created") {
      this.fileList = [...this.fileList, event.file_name].sort();
      this.changeLog.push(event.event_type + " " + event.file_name);
    } else if (event.event_type === "deleted") {
      const index = this.fileList.indexOf(event.file_name);
      if (index > -1) {
        this.fileList.splice(index, 1);
        this.changeLog.push(event.event_type + " " + event.file_name);
      }
    } else {      
      source.close();
    }
  }

  clearAndStop(){
    this.eventService.closeConnection().subscribe(data => {      
      this.fileList = [];
      this.changeLog = [];
      this.watchFlag = !this.watchFlag;
      this.stopFlag = !this.stopFlag;
    });
  }

}
