<script setup>
// 会话锁卷开关：纯前端内存状态，切换时不发任何请求（不落库、不产生 calc_runs）
defineProps({ modelValue: Boolean })
const emit = defineEmits(['update:modelValue'])
function onToggle(e) { emit('update:modelValue', e.target.checked) }
</script>
<template>
  <label class="roll-lock" :title="modelValue ? '已锁定：切换墙面保持当前卷' : '未锁定：切换墙面回到系统默认卷'">
    <input type="checkbox" :checked="modelValue" @change="onToggle" />
    锁卷{{ modelValue ? '·已锁' : '' }}
  </label>
</template>
