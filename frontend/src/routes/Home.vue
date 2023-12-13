<template>
    <div style="min-height: 100%;">
        <div style="padding-top: 40vh;">
            <a-input-search
            v-model:value="value"
            placeholder="input tracking number"
            enter-button
            style="width: 250px"
            @search="onSearch"
            />
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

const value = ref('')

onMounted(() =>{
    Cookies.set('DATA', null)
})
const onSearch = (e) =>{
    let data = {
        package_code: e
    }
    console.log(data)

    axios.post(apiHead() + ':8005/lockers/pickup', data)
    // axios.post('http://localhost:8005/lockers/pickup',data)
    .then((res) =>{
        console.log(res)
        message.success(res.data.msg)
        value.value = ""
        Cookies.set('DATA', JSON.stringify(data))
        console.log(JSON.parse(Cookies.get('DATA')))
        router.push('/pick')
    })
    .catch((err) =>{
        message.error('Invalid Tracking Number')
        value.value = ""
    })
}
</script>