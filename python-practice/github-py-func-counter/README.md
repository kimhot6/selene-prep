# Github Py Func Counter

github 원격 저장소를 임시 폴더에 clone 해와서 저장소 안 .py 파일들의 함수 개수를 count 해주는 도구입니다.

## 기능

- 파일의 상대경로 출력
- 파일별 함수 개수 출력

## 요구 사항

```bash
pip install pandas
```

## 사용법

```bash
python3 count_functions.py <분석할 Github 저장소 주소>
```

## 예시 결과

Flask 오픈소스 프로젝트 분석 결과 예시입니다:

```text
==========================================================================
   NUMBER OF FUNCTIONS IN PYTHON FILES
==========================================================================
docs/conf.py                                                         2
examples/celery/make_celery.py                                       0
examples/celery/src/task_app/__init__.py                             4
examples/celery/src/task_app/tasks.py                                3
examples/celery/src/task_app/views.py                                4
examples/javascript/js_example/__init__.py                           0
examples/javascript/js_example/views.py                              2
examples/javascript/tests/conftest.py                                2
examples/javascript/tests/test_js_example.py                         3
examples/tutorial/flaskr/__init__.py                                 2
examples/tutorial/flaskr/auth.py                                     6
examples/tutorial/flaskr/blog.py                                     5
examples/tutorial/flaskr/db.py                                       5
examples/tutorial/tests/conftest.py                                  7
examples/tutorial/tests/test_auth.py                                 5
examples/tutorial/tests/test_blog.py                                 8
examples/tutorial/tests/test_db.py                                   3
examples/tutorial/tests/test_factory.py                              2
src/flask/__init__.py                                                0
src/flask/__main__.py                                                0
src/flask/app.py                                                    40
src/flask/blueprints.py                                              4
src/flask/cli.py                                                    36
src/flask/config.py                                                 14
src/flask/ctx.py                                                    28
src/flask/debughelpers.py                                            7
src/flask/globals.py                                                 2
src/flask/helpers.py                                                23
src/flask/json/__init__.py                                           5
src/flask/json/provider.py                                          11
src/flask/json/tag.py                                               34
src/flask/logging.py                                                 3
src/flask/sansio/app.py                                             39
src/flask/sansio/blueprints.py                                      40
src/flask/sansio/scaffold.py                                        35
src/flask/sessions.py                                               22
src/flask/signals.py                                                 0
src/flask/templating.py                                             15
src/flask/testing.py                                                12
src/flask/typing.py                                                  0
src/flask/views.py                                                   6
src/flask/wrappers.py                                               12
tests/conftest.py                                                   13
tests/test_appctx.py                                                35
tests/test_apps/blueprintapp/__init__.py                             0
tests/test_apps/blueprintapp/apps/__init__.py                        0
tests/test_apps/blueprintapp/apps/admin/__init__.py                  2
tests/test_apps/blueprintapp/apps/frontend/__init__.py               2
tests/test_apps/cliapp/__init__.py                                   0
tests/test_apps/cliapp/app.py                                        0
tests/test_apps/cliapp/factory.py                                    3
tests/test_apps/cliapp/importerrorapp.py                             0
tests/test_apps/cliapp/inner1/__init__.py                            0
tests/test_apps/cliapp/inner1/inner2/__init__.py                     0
tests/test_apps/cliapp/inner1/inner2/flask.py                        0
tests/test_apps/cliapp/multiapp.py                                   0
tests/test_apps/helloworld/hello.py                                  1
tests/test_apps/helloworld/wsgi.py                                   0
tests/test_apps/subdomaintestmodule/__init__.py                      0
tests/test_async.py                                                 19
tests/test_basic.py                                                249
tests/test_blueprints.py                                           165
tests/test_cli.py                                                   68
tests/test_config.py                                                18
tests/test_converters.py                                             7
tests/test_helpers.py                                               51
tests/test_instance_config.py                                        8
tests/test_json.py                                                  38
tests/test_json_tag.py                                               9
tests/test_logging.py                                                9
tests/test_regression.py                                             4
tests/test_reqctx.py                                                30
tests/test_request.py                                                6
tests/test_session_interface.py                                      4
tests/test_signals.py                                               25
tests/test_subclassing.py                                            3
tests/test_templating.py                                            80
tests/test_testing.py                                               47
tests/test_user_error_handler.py                                    44
tests/test_views.py                                                 44
tests/type_check/typing_app_decorators.py                            6
tests/type_check/typing_error_handler.py                             4
tests/type_check/typing_route.py                                    18
CSV 저장 완료: results/function_number.csv (83개 파일)
```

## 사용 기술

- Python 3
- `ast` module (Abstract Syntax Tree)
- `pandas`
- `pathlib`
