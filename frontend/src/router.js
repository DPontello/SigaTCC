import { createRouter, createWebHistory } from 'vue-router'

import AcademicUnitsPage from './pages/AcademicUnitsPage.vue'
import CoursesPage from './pages/CoursesPage.vue'
import DashboardPage from './pages/DashboardPage.vue'
import DepartmentsPage from './pages/DepartmentsPage.vue'
import ProfessorsPage from './pages/ProfessorsPage.vue'
import StudentsPage from './pages/StudentsPage.vue'
import TccsPage from './pages/TccsPage.vue'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: DashboardPage,
  },
  {
    path: '/tccs',
    name: 'tccs',
    component: TccsPage,
  },
  {
    path: '/alunos',
    name: 'students',
    component: StudentsPage,
  },
  {
    path: '/professores',
    name: 'professors',
    component: ProfessorsPage,
  },
  {
    path: '/cursos',
    name: 'courses',
    component: CoursesPage,
  },
  {
    path: '/departamentos',
    name: 'departments',
    component: DepartmentsPage,
  },
  {
    path: '/unidades-academicas',
    name: 'academic-units',
    component: AcademicUnitsPage,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router