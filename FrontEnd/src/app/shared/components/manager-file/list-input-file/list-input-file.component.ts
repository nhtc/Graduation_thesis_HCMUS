import { Component, OnInit } from '@angular/core';
import { MessageService } from '@app/core/services/Utils/message.service';
import { UploadChangeParam, NzUploadModule, UploadFile, NzUploadComponent } from 'ng-zorro-antd/upload';

import { NzMessageService } from 'ng-zorro-antd/message';
import { FileService } from '@../../../src/app/shell/shell-routing-service';
import { RouterModule, Router } from '@angular/router';
@Component({
  selector: 'app-list-input-file',
  templateUrl: './list-input-file.component.html',
  styleUrls: ['./list-input-file.component.scss'],
})
export class ListInputFileComponent implements OnInit {
  statusList = [
    { text: 'Chờ', value: 'Peding' },
    { text: 'Thành công', value: 'Sucess' },
    { text: 'Thất bại', value: 'Error' },
  ];
  isvalid: boolean = false;

  msg: NzMessageService;
  sortValue: any = null;
  sortName: any = null;
  listOfSearchName: any = [];
  searchAddress: string;
  displayData: Array<object> = [];
  loading = true;
  FileToUpload: File = null;
  ListFileToUpload: FileList = null;
  data = [
    {
      name: 'Hoàn thiện các giải pháp QLNN đối với các hoạt động tôn giáo ở Việt Nam trong thời kỳ đổi mới.docx',
      status: 'Thất bại',
    },
    {
      name: 'Quản lý nhà nước đối với tập đoàn kinh tế tư nhân ở Việt Nam hiện nay.pdf',
      status: 'Chờ',
    },
    {
      name: 'Quản lý nhà nước về văn thư, lưu trữ.docx',
      status: 'Thất bại',
    },
    {
      name: 'Quản lý nhà nước về quy hoạch xây dựng nông thôn mới.docx',
      status: 'Thành công',
    },
  ];
  fileList: Array<object> = [];
  constructor(private messageService: MessageService, private fileService: FileService, private router: Router) {}
  ngOnInit(): void {
    this.getData();
  }

  getData(): void {
    const number = Math.floor(Math.random() * 100);
    setTimeout(() => {
      this.displayData = [...this.data];
      this.loading = false;
    }, number);
  }
  sort(sort: { key: string; value: string }): void {
    this.sortName = sort.key;
    this.sortValue = sort.value;
    this.search();
  }

  filter(listOfSearchName: string[], searchAddress: string): void {
    this.listOfSearchName = listOfSearchName;
    this.searchAddress = searchAddress;
    this.search();
  }

  search(): void {
    // filter data
    const filterFunc = (item: any) =>
      (this.searchAddress ? item.address.indexOf(this.searchAddress) !== -1 : true) &&
      (this.listOfSearchName.length
        ? this.listOfSearchName.some((name: string) => item.name.indexOf(name) !== -1)
        : true);
    const data = this.data.filter((item) => filterFunc(item));
    // sort data
    if (this.sortName && this.sortValue) {
      this.displayData = data.sort((a, b) =>
        this.sortValue === 'ascend'
          ? a[this.sortName] > b[this.sortName]
            ? 1
            : -1
          : b[this.sortName] > a[this.sortName]
          ? 1
          : -1
      );
    } else {
      this.displayData = data;
    }
  }

  /**
   * Upload file to server
   */
  upload = (file: any) => {
    console.log('welcome');
    console.log(file.name);
    console.log(file);
    /*setTimeout(() => {
      file.onProgress({ percent: 50 });
      setTimeout(() => {
        const dataFile = {
          name: file.file.name,
          status: 'Thành công'
        };
        this.data.push(dataFile);
        // notify success
        file.onSuccess();
        this.displayData = [...this.data];
        this.messageService.success('Thêm tệp tin thành công');
      }, 500);
    }, 10);*/
    // tslint:disable-next-line:semicolon
    this.fileService.UploadFile(file);
  };
  /* uploadFile = ((file: NzUploadFile) => {
    console.log('welcome to upload');
    /*console.log(file.name);
    console.log(file);
    this.FileToUpload = file;
    this.invalid();
    console.log(this.isvalid);
    console.log(file);
    this.FileToUpload = file;
    /*setTimeout(() => {
      file.onProgress({ percent: 50 });
      setTimeout(() => {
        const dataFile = {
          name: file.file.name,
          status: 'Thành công'
        };
        this.data.push(dataFile);
        // notify success
        file.onSuccess();
        this.displayData = [...this.data];
        this.messageService.success('Thêm tệp tin thành công');
      }, 500);
    }, 10);
    this.fileService.UploadFile(this.FileToUpload).subscribe(data => {
      console.log(data);
    });
    // tslint:disable-next-line:semicolon
  };*/
  uploadFile = (file: UploadFile) => {
    console.log('welcome to upload');
    console.log(file.name);
    console.log(file);
    this.FileToUpload = file.this.invalid();
    console.log(this.isvalid);

    setTimeout(() => {
      file.onProgress({ percent: 50 });
      setTimeout(() => {
        const dataFile = {
          name: file.file.name,
          status: 'Thành công',
        };
        this.data.push(dataFile);
        // notify success
        file.onSuccess();
        this.displayData = [...this.data];
        this.messageService.success('Thêm tệp tin thành công');
      }, 500);
    }, 10);
    this.fileService.UploadFile(this.FileToUpload).subscribe((data) => {
      console.log(data);
    });
    // tslint:disable-next-line:semicolon
  };
  uploadFileList = () => {
    this.invalid();

    /*setTimeout(() => {
      file.onProgress({ percent: 50 });
      setTimeout(() => {
        const dataFile = {
          name: file.file.name,
          status: 'Thành công'
        };
        this.data.push(dataFile);
        // notify success
        file.onSuccess();
        this.displayData = [...this.data];
        this.messageService.success('Thêm tệp tin thành công');
      }, 500);
    }, 10);*/
    this.fileService.UploadFileList(this.ListFileToUpload).subscribe((data) => {
      console.log(data);
    });

    // tslint:disable-next-line:semicolon
  };
  invalid() {
    if (this.FileToUpload != null && this.ListFileToUpload != null) this.isvalid = true;
    else this.isvalid = false;
  }
  /*handleChange(info: UploadChangeParam): void {
    this.uploadFileList(null);
    if (info.file.status !== 'uploading') {
      console.log(info.file, info.fileList);
    }
    if (info.file.status === 'done') {
      this.msg.success(`${info.file.name} file uploaded successfully`);
    } else if (info.file.status === 'error') {
      this.msg.error(`${info.file.name} file upload failed.`);
    }
  }*/
  handleChange(file: FileList): void {
    //this.FileToUpload=file.item(0);
    //this.uploadFile();
    this.ListFileToUpload = file;
    this.uploadFileList();
  }
  checkPlagism() {
    console.log('can go here');
    this.router.navigate(['checkresult/step/1'], { replaceUrl: true });
  }
}
