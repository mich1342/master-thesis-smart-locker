<template>
    <div style="min-height: 100%;">
        <div style="padding-top: 35vh;">
            
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
            <a-button v-if="!startScan" @click="startScan=true" type="primary">Scan Location</a-button>
            <div v-else class="stream">
              <qr-stream @decode="onDecode" class="mb">
                <div style="color: red;" class="frame"></div>
              </qr-stream>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import {apiHead} from '../helper'
import {message} from 'ant-design-vue'
import {QrStream} from 'vue3-qr-reader'

const trackingNumber = ref('')
const lockerCode = ref('')
const startScan = ref(false)
const onDecode = (e) =>{
    
    let data = {
        locker: e.split('/')[0],
        box: e.split('/')[1],
        package_code: trackingNumber.value
    }
    console.log(data)
    axios.post(apiHead() + ':8005/lockers/assign', data)
    .then((res) =>{
        console.log(res)
        message.success(res.data.msg)
        trackingNumber.value = ""
        lockerCode.value = ""
        startScan.value = false
    })
    .catch((err) =>{
        message.error('Invalid Tracking Number')
        trackingNumber.value = ""
        lockerCode.value = ""
        startScan.value = false
    })
}
</script>