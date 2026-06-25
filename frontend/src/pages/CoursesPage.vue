<script setup>
import { onMounted, ref, computed } from 'vue'
import { tccApi } from '../services/tccApi'

const courses = ref([])
const isLoading = ref(true)
const errorMessage = ref('')
const searchQuery = ref('')

const filteredCourses = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return courses.value
  return courses.value.filter(c =>
    c.nome.toLowerCase().includes(q) ||
    c.sigla.toLowerCase().includes(q) ||
    c.codigo.toLowerCase().includes(q)
  )
})

async function loadCourses() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const response = await tccApi.getCourses()
    courses.value = response.data
  } catch (error) {
    errorMessage.value = 'Não foi possível carregar os cursos. Verifique se o backend está rodando.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

onMounted(loadCourses)
</script>

<template>
  <section class="page">
    <header class="page-header">
      <div>
        <h1>Cursos</h1>
        <p>Consulta de cursos cadastrados.</p>
      </div>
    </header>

    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Filtrar por nome, sigla ou código..."
      />
    </div>

    <div v-if="isLoading" class="status-box">
      Carregando cursos...
    </div>

    <div v-else-if="errorMessage" class="status-box status-box-error">
      {{ errorMessage }}
    </div>

    <div v-else-if="filteredCourses.length === 0" class="status-box">
      Nenhum curso encontrado.
    </div>

    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>Sigla</th>
            <th>Código</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="curso in filteredCourses" :key="curso.id">
            <td>{{ curso.nome }}</td>
            <td>{{ curso.sigla }}</td>
            <td>{{ curso.codigo }}</td>
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
