<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON, postJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'
import RollSelect from '../components/RollSelect.vue'
import RollLockToggle from '../components/RollLockToggle.vue'
const walls = ref([]); const rolls = ref([]); const wallId = ref(null); const rollId = ref(null)
const defaultRollId = ref(null)
// 锁卷状态只活在当前会话：仅存内存，不落墙面表字段，切换本身不产生 calc_runs
const rollLocked = ref(false)
const out = ref(null)
onMounted(async () => {
  walls.value = (await getJSON('/api/walls')).items.filter(w => w.data_quality==='clean')
  rolls.value = (await getJSON('/api/rolls')).items.filter(r => r.data_quality==='clean')
  const defaults = await getJSON('/api/session/defaults')
  defaultRollId.value = defaults.default_roll_id ?? rolls.value[0]?.id ?? null
  if (walls.value.length) wallId.value = walls.value[0].id
  rollId.value = defaultRollId.value
})
// 未锁定：切换墙面时卷材回到系统默认卷；锁定：保持当前选中卷材不变
watch(wallId, () => { if (!rollLocked.value) rollId.value = defaultRollId.value })
async function run(save) {
  out.value = save ? await postJSON('/api/estimate', { wall_id: wallId.value, roll_id: rollId.value, save: true }) : await getJSON(`/api/estimate?wall_id=${wallId.value}&roll_id=${rollId.value}`)
}
</script>
<template>
  <div class="page"><h1>算卷工作台</h1>
  <select v-model.number="wallId"><option v-for="w in walls" :key="w.id" :value="w.id">{{ w.name }}</option></select>
  <RollSelect v-model="rollId" :rolls="rolls" />
  <RollLockToggle v-model="rollLocked" />
  <button @click="run(false)">试算</button><button @click="run(true)">保存</button>
  <div v-if="out"><strong>{{ out.rolls }} 卷</strong> · {{ out.drops }} 条 · 每条 {{ out.drop_len_m }}m
  <DropStripBar :drops="out.drops" :drop-len="out.drop_len_m" :rolls="out.rolls" /></div>
  </div>
</template>
