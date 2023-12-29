<template>
    <div style="min-height: 100%;">
        <div style="padding-top: 5vh;">
            
            <a-input
            v-model:value="trackingNumber"
            placeholder="input tracking number"
            style="width: 250px"
            />
            <br/>
            <br/>
            <!-- <a-input-search
            v-model:value="lockerCode"
            placeholder="input locker code"
            enter-button
            style="width: 250px"
            @search="onSearch"
            /> -->
            <a-button v-if="!startScan" @click="openScan" type="primary">Scan Location</a-button>
            <br />
            <br />
            <div id="qr-code-full-region">
              <!-- <qr-stream @decode="onDecode" class="mb">
                <div style="color: red;" class="frame"></div>
              </qr-stream> -->
              

            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import {apiHead} from '../helper'
import {message} from 'ant-design-vue'
import {QrStream} from 'vue3-qr-reader'
import {Html5QrcodeScanner} from 'html5-qrcode'

import successFile from '../assets/beep-success.mp3'
import failedFile from '../assets/beep-failed.mp3'
const audioSuccess = new Audio(successFile)
const audioFailed = new Audio(failedFile)
audioSuccess.autoplay = true
audioFailed.autoplay = true
const trackingNumber = ref('')
const lockerCode = ref('')
const startScan = ref(false)
const config = {
        fps: 10,
        qrbox: 200,
        rememberLastUsedCamera: true,
        aspectRatio: 4/3,
        showTorchButtonIfSupported: true,
        showZoomSliderIfSupported: true,
        defaultZoomValueIfSupported: 2
    }
var html5QrcodeScanner = null
onMounted(() =>{

    html5QrcodeScanner = new Html5QrcodeScanner('qr-code-full-region', config);
})
const openScan = () =>{
    startScan.value=true
    html5QrcodeScanner.render(onDecode);
}

const onScanSuccess = (decodedText, decodedResult) =>{
    alert(decodedText)
    console.log(decodedText)
}
const onDecode = (e) =>{
    let data = {
        locker: e.split('/')[0],
        box: e.split('/')[1],
        package_code: trackingNumber.value
    }
    axios.post(apiHead() + '/lockers/assign', data)
    .then((res) =>{
        audioSuccess.play()
        console.log(res)
        message.success(res.data.msg)
        trackingNumber.value = ""
        lockerCode.value = ""
        startScan.value = false
        // location.reload()
    })
    .catch((err) =>{
        audioFailed.play()
        message.error('Invalid Tracking Number')
        trackingNumber.value = ""
        lockerCode.value = ""
        startScan.value = false
    })
    router.push('/assign')
}
</script>
