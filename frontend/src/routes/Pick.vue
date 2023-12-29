<template>
    <div style="min-height: 100%;">
        <div style="padding-top: 5vh; padding-left: 5vw; padding-right: 5vw;">
            <a-typography-title :level="2">
                Please claim your package at Locker {{ transactionData.locker }}, Box {{ transactionData.box }}
            </a-typography-title>
            <br/>

            <a-button v-if="!startScan" type="primary" @click="openScan">Scan</a-button>
            <div v-else class="stream">
                <!-- <qr-stream @decode="onDecode" class="mb">
                    <div style="color: green;" class="frame"></div>
                    
                </qr-stream> -->
                
                <br/>
                <a-typography-title :level="5">Scan QR Code on the Locker</a-typography-title>
            </div>
            <div id="qr-code-full-region">
            </div>
            <br/>
            <br/>
            <a-button type="primary" @click="pingButton">Ping</a-button>
            <br/>
            <br/>
            <div v-if="scanDone">
                <a-typography-title :level="3">
                    Report problem if the door is not open
                </a-typography-title>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import {apiHead} from '../helper'
import {message} from 'ant-design-vue'
import Cookies from 'js-cookie'
import router from '../router'
import {QrStream} from 'vue3-qr-reader'
import {Html5QrcodeScanner} from 'html5-qrcode'
import successFile from '../assets/beep-success.mp3'
import failedFile from '../assets/beep-failed.mp3'
const audioSuccess = new Audio(successFile)
const audioFailed = new Audio(failedFile)

const transactionData = ref({})
const startScan = ref(false)
const scanValue = ref()
const scanDone = ref(false)

const config = {
        fps: 10,
        qrbox: 100,
        rememberLastUsedCamera: true,
        aspectRatio: 4/3,
        showTorchButtonIfSupported: true,
        showZoomSliderIfSupported: true,
        defaultZoomValueIfSupported: 2
    }
var html5QrcodeScanner = null
const openScan = () =>{
    startScan.value=true
    html5QrcodeScanner.render(onDecode);
}

const onDecode = (data) =>{
    scanValue.value = data
    let apiData = JSON.parse(Cookies.get('DATA'))
    apiData.qr_code = data
    console.log(apiData)
    axios.post(apiHead() + '/lockers/open_door', apiData)
    .then((res) =>{
        audioSuccess.play()
        console.log(res)
        message.success(res.data.msg)
        startScan.value = false
        scanDone.value = true
    })
    .catch((err) =>{
        audioFailed.play()
        message.error('Invalid QR Code')
    })
}
onMounted(() =>{
    html5QrcodeScanner = new Html5QrcodeScanner('qr-code-full-region', config);
    refreshData()
})
const refreshData = () =>{
    let data = JSON.parse(Cookies.get('DATA'))
    axios.post(apiHead() + '/lockers/pickup', data)
    .then((res) =>{
        console.log(res)
        transactionData.value = res.data.data
    })
    .catch((err) =>{
        message.error('Invalid Tracking Number')
        router.push('/')
    })
}
const pingButton = () =>{
    let data = JSON.parse(Cookies.get('DATA'))
    axios.post(apiHead() + '/lockers/ping', data)
    .then((res) =>{
        console.log(res)
        message.success(res.data.msg)
    })
    .catch((err) =>{
        message.error('Invalid Tracking Number')
        router.push('/')
    })
}

</script>
