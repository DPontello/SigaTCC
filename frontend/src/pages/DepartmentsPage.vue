<script setup>
import { onMounted, ref, computed } from 'vue'
import { tccApi } from '../services/tccApi'

const departments = ref([])
const unidades = ref([])
const isLoading = ref(true)
const errorMessage = ref('')
const searchQuery = ref('')

function getUnidadeNome(unidadeId) {
  const u = unidades.value.find(u => u.id === unidadeId)
  return u ? u.nome : `#${unidadeId}`
}

const filteredDepartments = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return departments.value
  return departments.value.filter(d =>
    d.nome.toLowerCase().includes(q) ||
    d.sigla.toLowerCase().includes(q) ||
    (getUnidadeNome(d.unidade_academica) || '').toLowerCase().includes(q)
  )
})

async function loadDepartments() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const [deptsRes, unitsRes] = await Promise.all([
      tccApi.getDepartments(),
      tccApi.getAcademicUnits(),
    ])
    departments.value = deptsRes.data
    unidades.value = unitsRes.data
  } catch (error) {
    errorMessage.value = 'Não foi possível carregar os departamentos. Verifique se o backend está rodando.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

onMounted(loadDepartments)
</script>

<template>
  <section class="page">
    <header class="page-header">
      <div>
        <h1>Departamentos</h1>
        <p>Consulta de departamentos cadastrados.</p>
      </div>
    </header>

    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Filtrar por nome, sigla ou unidade acadêmica..."
      />
    </div>

    <div v-if="isLoading" class="status-box">
      Carregando departamentos...
    </div>

    <div v-else-if="errorMessage" class="status-box status-box-error">
      {{ errorMessage }}
    </div>

    <div v-else-if="filteredDepartments.length === 0" class="status-box">
      Nenhum departamento encontrado.
    </div>

    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>Sigla</th>
            <th>Unidade Acadêmica</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="dept in filteredDepartments" :key="dept.id">
            <td>{{ dept.nome }}</td>
            <td>{{ dept.sigla }}</td>
            <td>{{ getUnidadeNome(dept.unidade_academica) }}</td>
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
