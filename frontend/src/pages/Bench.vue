<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON, postJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'
import RollSelect from '../components/RollSelect.vue'
import RollLockToggle from '../components/RollLockToggle.vue'
const walls = ref([]); const rolls = ref([])
const wallId = ref(null); const rollId = ref(null); const defaultRollId = ref(null)
// 会话锁卷状态：仅存在内存，刷新即失；不落墙面表、不写 calc_runs
const locked = ref(false)
const out = ref(null)
onMounted(async () => {
  const [w, r, s] = await Promise.all([
    getJSON('/api/walls'), getJSON('/api/rolls'), getJSON('/api/session/bench'),
  ])
  walls.value = w.items.filter(x => x.data_quality === 'clean')
  rolls.value = r.items.filter(x => x.data_quality === 'clean')
  defaultRollId.value = s.default_roll_id
  rollId.value = s.default_roll_id
  if (walls.value.length) wallId.value = walls.value[0].id
})
// 切换墙面：锁卷时保持当前卷，未锁时回到系统默认卷
watch(wallId, () => { if (!locked.value && defaultRollId.value != null) rollId.value = defaultRollId.value })
async function run(save) {
  out.value = save ? await postJSON('/api/estimate', { wall_id: wallId.value, roll_id: rollId.value, save: true }) : await getJSON(`/api/estimate?wall_id=${wallId.value}&roll_id=${rollId.value}`)
}
</script>
<template>
  <div class="page"><h1>算卷工作台</h1>
  <select v-model.number="wallId"><option v-for="w in walls" :key="w.id" :value="w.id">{{ w.name }}</option></select>
  <RollSelect v-model="rollId" :rolls="rolls" />
  <RollLockToggle v-model="locked" />
  <button @click="run(false)">试算</button><button @click="run(true)">保存</button>
  <div v-if="out"><strong>{{ out.rolls }} 卷</strong> · {{ out.drops }} 条 · 每条 {{ out.drop_len_m }}m
  <DropStripBar :drops="out.drops" :drop-len="out.drop_len_m" :rolls="out.rolls" /></div>
  </div>
</template>
