const { ipcRenderer } = require('electron')

const sendEvent = async ()=>{
    let fallback = await ipcRenderer.invoke('send-event','hahahaha')
    console.log(fallback)
}