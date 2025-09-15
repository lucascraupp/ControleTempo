# Diagrama de Relacionamento das Entidades - ControleTempo

```mermaid
erDiagram
    Users ||--o{ AreasOfLife : "cria"
    Users ||--o{ Projects : "cria"
    Users ||--o{ Tasks : "cria"
    Users ||--o{ ProjectsHasAreasOfLife : "associa"
    Users ||--o{ UsersHasTasks : "gerencia"

    AreasOfLife ||--o{ ProjectsHasAreasOfLife : "está em"
    AreasOfLife ||--o{ TasksHasAreasOfLife : "está em"

    Projects ||--o{ ProjectsHasAreasOfLife : "pertence a"
    
    Tasks ||--o{ UsersHasTasks : "é gerenciada por"
    
    ProjectsHasAreasOfLife ||--o{ TasksHasProjects : "é associado em"

    UsersHasTasks ||--o{ TasksHasAreasOfLife : "relaciona com"
    UsersHasTasks ||--o{ TasksHasProjects : "relaciona com"

    TasksHasAreasOfLife }o--|| AreasOfLife : "pertence a"

    TasksHasProjects }o--|| ProjectsHasAreasOfLife : "pertence a"

    Users {
        integer id PK
        string name
        datetime created_at
    }

    AreasOfLife {
        integer id PK
        string name
        integer who_created FK "Users.id"
    }

    Projects {
        integer id PK
        string name
        integer who_created FK "Users.id"
    }

    Tasks {
        integer id PK
        string name
        integer who_created FK "Users.id"
    }

    ProjectsHasAreasOfLife {
        integer user_id PK,FK "Users.id"
        integer area_of_life_id PK,FK "AreasOfLife.id"
        integer project_id PK,FK "Projects.id"
        datetime created_at
    }

    UsersHasTasks {
        integer user_id PK,FK "Users.id"
        integer task_id PK,FK "Tasks.id"
        datetime created_at
    }

    TasksHasAreasOfLife {
        integer user_id PK,FK "UsersHasTasks.user_id"
        integer task_id PK,FK "UsersHasTasks.task_id"
        integer area_of_life_id PK,FK "AreasOfLife.id"
        datetime created_at
    }

    TasksHasProjects {
        integer user_id PK,FK "UsersHasTasks.user_id"
        integer task_id PK,FK "UsersHasTasks.task_id" 
        integer area_of_life_id PK,FK "ProjectsHasAreasOfLife.area_of_life_id"
        integer project_id PK,FK "ProjectsHasAreasOfLife.project_id"
        datetime created_at
    }
```