basic_searchs = {
            'nodejs': {
                'search_queries': [
                    'filename:package.json "@cucumber/cucumber"',
                    'filename:package.json "cucumber"',
                    'language:javascript cucumber',
                    'language:typescript cucumber'
                ]
            },
            'java': {
                'search_queries': [
                    'filename:pom.xml "io.cucumber"',
                    'filename:build.gradle cucumber-java',
                    'language:java cucumber'
                ]
            },
            'ruby': {
                'search_queries': [
                    'filename:Gemfile cucumber',
                    'language:ruby cucumber'
                ]
            },
            'kotlin': {
                'search_queries': [
                    'language:kotlin cucumber',
                    'filename:build.gradle.kts cucumber'
                ]
            },
            'scala': {
                'search_queries': [
                    'language:scala cucumber',
                    'filename:build.sbt cucumber'
                ]
            },
            'go': {
                'search_queries': [
                    'language:go godog',
                    'filename:go.mod godog'
                ]
            },
            'android': {
                'search_queries': [
                    'filename:build.gradle cucumber-android',
                    'language:java cucumber-android'
                ]
            },
            'lua': {
                'search_queries': [
                    'language:lua cucumber'
                ]
            },
            'cpp': {
                'search_queries': [
                    'language:cpp cucumber',
                    'cucumber-cpp'
                ]
            },
            'ocaml': {
                'search_queries': [
                    'language:ocaml cucumber',
                    'cucumber.ml'
                ]
            }
        }
