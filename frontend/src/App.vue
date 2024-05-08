<template>
<a-layout style="min-height: 100vh;">
  <a-layout-header style="text-align: center; background-color: #003877;">
    <div style="font-size: x-large; font-weight: bolder; color: #F3F6F4;">
      Smart Locker
    </div>
  </a-layout-header>
  <a-layout-content style="background-color: #F3F6F4;">
    <a-row>
      <a-col :xs="0" :sm="0" :md="0" :lg="6" :xl="6" />
      <a-col :xs="24" :sm="24" :md="24" :lg="12" :xl="12" style="text-align: center;">
        <router-view/>
      </a-col>
      <a-col :xs="0" :sm="0" :md="0" :lg="6" :xl="6" />
    </a-row>
  </a-layout-content>
  <a-layout-footer style="text-align: center;">
    Smart Locker System ©2024 
  </a-layout-footer>
</a-layout>
</template>

<script setup>
</script>
