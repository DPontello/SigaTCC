<script setup>
import { onMounted, ref, computed } from 'vue'
import { tccApi } from '../services/tccApi'

const units = ref([])
const isLoading = ref(true)
const errorMessage = ref('')
const searchQuery = ref('')

const filteredUnits = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return units.value
  return units.value.filter(u =>
    u.nome.toLowerCase().includes(q) ||
    u.sigla.toLowerCase().includes(q)
  )
})

async function loadUnits() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const response = await tccApi.getAcademicUnits()
    units.value = response.data
  } catch (error) {
    errorMessage.value = 'Não foi possível carregar as unidades acadêmicas. Verifique se o backend está rodando.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

onMounted(loadUnits)
</script>

<template>
  <section class="page">
    <header class="page-header">
      <div>
        <h1>Unidades Acadêmicas</h1>
        <p>Consulta de unidades acadêmicas cadastradas.</p>
      </div>
    </header>

    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Filtrar por nome ou sigla..."
      />
    </div>

    <div v-if="isLoading" class="status-box">
      Carregando unidades acadêmicas...
    </div>

    <div v-else-if="errorMessage" class="status-box status-box-error">
      {{ errorMessage }}
    </div>

    <div v-else-if="filteredUnits.length === 0" class="status-box">
      Nenhuma unidade acadêmica encontrada.
    </div>

    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>Sigla</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="unit in filteredUnits" :key="unit.id">
            <td>{{ unit.nome }}</td>
            <td>{{ unit.sigla }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
.search-bar {
  display: flex;
  gap: 8px;
}

.search-bar input {
  flex: 1;
  border: 1px solid #c9d4e5;
  border-radius: 8px;
  padding: 10px 14px;
  background: #ffffff;
  font: inherit;
}

.table-container {
  border: 1px solid #dfe5ee;
  border-radius: 8px;
  background: #ffffff;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 12px 16px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #667085;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #edf1f7;
}

td {
  padding: 12px 16px;
  border-bottom: 1px solid #edf1f7;
  color: #17202a;
}

tr:last-child td {
  border-bottom: 0;
}
</style>
