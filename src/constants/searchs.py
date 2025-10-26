searchs = {
    'nodejs': {
        'files': ['package.json'],
        'content_patterns': ['"@cucumber/cucumber"', '"cucumber"'],
        'search_queries': ['filename:package.json "@cucumber/cucumber"',
                           'language:javascript cucumber feature']
    },
    'java': {
        'files': ['pom.xml', 'build.gradle'],
        'content_patterns': ['io.cucumber', 'cucumber-java'],
        'search_queries': ['filename:pom.xml "io.cucumber"',
                           'filename:build.gradle cucumber-java',
                           'language:java cucumber-java']
    },
    'ruby': {
        'files': ['Gemfile'],
        'content_patterns': ['cucumber'],
        'search_queries': ['filename:Gemfile "cucumber"',
                           'language:ruby cucumber feature']
    },
    'android': {
        'files': ['build.gradle', 'app/build.gradle'],
        'content_patterns': ['cucumber-android'],
        'search_queries': ['filename:build.gradle cucumber-android',
                           'language:java cucumber-android']
    },
    'kotlin': {
        'files': ['build.gradle.kts', 'build.gradle'],
        'content_patterns': ['cucumber-kotlin'],
        'search_queries': ['language:kotlin cucumber',
                           'filename:build.gradle.kts cucumber']
    },
    'lua': {
        'files': ['*.lua'],
        'content_patterns': ['cucumber'],
        'search_queries': ['language:lua cucumber']
    },
    'scala': {
        'files': ['build.sbt'],
        'content_patterns': ['cucumber-scala'],
        'search_queries': ['language:scala cucumber',
                           'filename:build.sbt cucumber']
    },
    'cpp': {
        'files': ['CMakeLists.txt', 'Makefile'],
        'content_patterns': ['cucumber-cpp'],
        'search_queries': ['language:cpp cucumber',
                           'cucumber-cpp']
    },
    'ocaml': {
        'files': ['dune', 'opam'],
        'content_patterns': ['cucumber.ml'],
        'search_queries': ['language:ocaml cucumber',
                           'cucumber.ml']
    },
    'golang': {
        'files': ['go.mod', 'go.sum'],
        'content_patterns': ['godog'],
        'search_queries': ['language:go godog',
                           'filename:go.mod godog']
    }
}
