<script setup>
// 会话锁卷开关：只翻转会话内状态，不发任何请求、不落库
defineProps({ modelValue: { type: Boolean, default: false } })
const emit = defineEmits(['update:modelValue'])
function onToggle(e) {
  emit('update:modelValue', e.target.checked)
}
</script>
<template>
  <label class="roll-lock-toggle">
    <input type="checkbox" :checked="modelValue" @change="onToggle" />
    锁卷：换墙保持当前卷材
  </label>
</template>
