<template>
  <div class="script-page">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800">自动化脚本</h2>
      <p class="text-gray-500 mt-1">编写和执行自动化脚本，实现全自动化操作</p>
    </div>
    
    <ScriptEditor />
  </div>
</template>

<script setup>
import ScriptEditor from '@/components/ScriptEditor.vue'
</script>
