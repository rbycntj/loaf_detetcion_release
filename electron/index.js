// Modules to control application life and create native browser window
const { Menu } = require('electron'); // 引入 Menu 模块
Menu.setApplicationMenu(null);
const {app, BrowserWindow} = require('electron')
const path = require('path')
const {ipcMain} = require('electron');
let mainWindow;
let choiceWindow;

ipcMain.on('main:choice', (event, arg) =>{
  choiceWindow = new BrowserWindow({
    resizable: false,
    width: 400,
    height: 500,
    parent: mainWindow,
    modal: true,
    show: false,
    webPreferences: {
      nodeIntegration:true,
      contextIsolation: false,
      preload: path.join(__dirname, './preload/preload.js')
    }
  })
  choiceWindow.loadFile('src\\choice.html').then(r => console.log(r))
  choiceWindow.once('ready-to-show', () => {
    choiceWindow.show()
  })
  choiceWindow.on('closed', () => {
    choiceWindow = null;
  });
})

ipcMain.on('send-data', (event, data) =>{
  mainWindow.webContents.send('record', data)
  setTimeout(function (){
    mainWindow.webContents.send('get_data', data)
  }, 2000)
})

function createWindow () {
  // Create the browser window.

  mainWindow = new BrowserWindow({
    resizable: false,
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration:true,
      contextIsolation: false,
      preload: path.join(__dirname , './preload/preload.js')
    }
  })

  // and load the index.html of the app.
  mainWindow.loadFile('src\\login.html').then(r => console.log(r))
  mainWindow.once('ready-to-show', () => {
    mainWindow.show()
  })
  // Open the DevTools.
  //mainWindow.webContents.openDevTools()
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
