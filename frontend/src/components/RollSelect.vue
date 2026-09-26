<script setup>
// 卷材下拉：纯展示组件，只负责列出可选卷材并回传选择
defineProps({
  rolls: { type: Array, default: () => [] },
  modelValue: { type: Number, default: null },
})
const emit = defineEmits(['update:modelValue'])
function onChange(e) {
  emit('update:modelValue', Number(e.target.value))
}
</script>
<template>
  <select :value="modelValue" @change="onChange">
    <option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }}</option>
  </select>
</template>
