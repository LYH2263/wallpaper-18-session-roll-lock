<script setup>
// 卷材下拉：纯受控组件，只负责列出可选卷并上报选择
defineProps({
  rolls: { type: Array, default: () => [] },
  modelValue: Number,
})
const emit = defineEmits(['update:modelValue'])
function onChange(e) { emit('update:modelValue', Number(e.target.value)) }
</script>
<template>
  <select :value="modelValue" @change="onChange">
    <option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }}</option>
  </select>
</template>
