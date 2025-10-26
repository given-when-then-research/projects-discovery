improved_searches = {
    'nodejs': {
        'search_queries': [
            # Pacotes principais do Cucumber para Node.js
            'filename:package.json "@cucumber/cucumber"',
            
            # Por linguagem específica
            'language:javascript @cucumber/cucumber',
            'language:typescript @cucumber/cucumber',
            'language:javascript cucumber',
            'language:typescript cucumber',
            
            # Arquivos de configuração específicos
            'path:features extension:feature',
            'filename:.feature language:gherkin'
        ]
    },
    'java': {
        'search_queries': [
            # Maven dependencies
            'filename:pom.xml "io.cucumber"',
            'filename:pom.xml "cucumber-java"',
            'filename:pom.xml "cucumber-junit"',
            
            # Gradle dependencies (diferentes sintaxes)
            'filename:build.gradle "io.cucumber"',
            'filename:build.gradle "cucumber-java"',
            'filename:build.gradle "cucumber-junit"',
            'filename:build.gradle.kts "io.cucumber"',
            'filename:build.gradle.kts "cucumber-java"',
            
            # Por linguagem
            'language:java cucumber',
            'language:java "io.cucumber"',
            
            # Arquivos de feature
            'language:java path:features extension:feature',
            'language:java "@CucumberOptions"'
        ]
    },
    'ruby': {
        'search_queries': [
            # Gemfile dependencies
            'filename:Gemfile "cucumber"',
            'filename:Gemfile "cucumber-rails"',
            'filename:Gemfile.lock "cucumber"',
            
            # Por linguagem
            'language:ruby cucumber',
            'language:ruby "cucumber-rails"',
            
            # Arquivos específicos do Rails
            'filename:cucumber.yml',
            'path:features/support language:ruby',
            'language:ruby "@cucumber"'
        ]
    },
    'kotlin': {
        'search_queries': [
            # Kotlin usando Cucumber-JVM
            'language:kotlin "io.cucumber"',
            'language:kotlin cucumber',
            'filename:build.gradle.kts "cucumber-java" language:kotlin',
            'filename:pom.xml "cucumber-java" language:kotlin',
            'language:kotlin "@CucumberOptions"'
        ]
    },
    'scala': {
        'search_queries': [
            # SBT dependencies
            'filename:build.sbt cucumber',
            'filename:build.sbt "io.cucumber"',
            
            # Por linguagem
            'language:scala cucumber',
            'language:scala "io.cucumber"',
            
            # Gradle/Maven para projetos Scala
            'filename:build.gradle "cucumber-scala"',
            'filename:pom.xml "cucumber-scala"'
        ]
    },
    'go': {
        'search_queries': [
            # Godog (implementação Go do Cucumber)
            'language:go godog',
            'filename:go.mod godog',
            'filename:go.sum godog',
            'language:go "github.com/cucumber/godog"',
            'import:"github.com/cucumber/godog"'
        ]
    },
    'android': {
        'search_queries': [
            # Android específico
            'filename:build.gradle "cucumber-android"',
            'filename:build.gradle.kts "cucumber-android"',
            'language:java "cucumber-android"',
            'language:kotlin "cucumber-android"',
            
            # Dependências relacionadas
            'filename:build.gradle "io.cucumber" "android"',
            'path:app/src/androidTest cucumber'
        ]
    },
    'lua': {
        'search_queries': [
            # Cucumber-Lua
            'language:lua cucumber',
            'language:lua "cucumber-lua"',
            'filename:rockspec cucumber'
        ]
    },
    'cpp': {
        'search_queries': [
            # C++ Cucumber
            'language:cpp cucumber',
            'language:c++ cucumber',
            '"cucumber-cpp"',
            'cucumber-cpp'
            'filename:CMakeLists.txt cucumber',
            'filename:Makefile cucumber-cpp'
        ]
    },
    'ocaml': {
        'search_queries': [
            # OCaml Cucumber
            'language:ocaml cucumber',
            'language:ocaml "cucumber.ml"',
            'cucumber.ml',
            'filename:dune cucumber',
            'filename:dune-project cucumber',
            'filename:opam cucumber'
        ]
    },
}