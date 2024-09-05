#!/bin/sh

HIGHPRIO_WORKER_NUM_PROCESSES=${HIGHPRIO_WORKER_NUM_PROCESSES:=0}
MEDPRIO_WORKER_NUM_PROCESSES=${MEDPRIO_WORKER_NUM_PROCESSES:=0}
LOWPRIO_WORKER_NUM_PROCESSES=${LOWPRIO_WORKER_NUM_PROCESSES:=0}

echo $1
echo $2

# The first input tell us what will be executed
case $1 in

"migrate")
  python manage.py migrate;;

"collectstatic")
    python manage.py collectstatic --no-input;;

# Using the keyword app it will be run the app
"app")
  # This script is prepared to be used in development too
  if echo $DJANGO_DEBUG | grep -i "^true$" > /dev/null ; then
    python manage.py migrate
    gunicorn config.wsgi --config="docker/gunicorn.dev.conf.py"
  else
    python manage.py collectstatic --no-input
    gunicorn config.wsgi --config="docker/gunicorn.conf.py"
  fi;;

# Using the keyword workers it will be run the workers attending to the second parameter
"workers")
      case "$2" in
            # High prio workers only attend to highprio queue, this queue must be free most of the time
            "high_priority")
                  echo "Running $HIGHPRIO_WORKER_NUM_PROCESSES high priority workers" &&
                  if [ $HIGHPRIO_WORKER_NUM_PROCESSES -gt 0 ]; then
                    HIGHPRIO_CONCURRENCY="--concurrency=${HIGHPRIO_WORKER_NUM_PROCESSES}"
                    celery -A config worker -n mani_highprio -Q highprio -l info ${HIGHPRIO_CONCURRENCY}
                  else
                    echo "There are no workers to set"
                  fi;;
            # Medium prio workers attend to highprio and medprio queues, also executes the beat and the default queue
            "medium_priority")
                  echo "Running $MEDPRIO_WORKER_NUM_PROCESSES medium priority workers"
                  if [ $MEDPRIO_WORKER_NUM_PROCESSES -gt 0 ]; then
                    MEDPRIO_CONCURRENCY="--concurrency=${MEDPRIO_WORKER_NUM_PROCESSES}"
                    celery -A config worker -n mani_medprio -Q highprio,medprio,celery -B -l info ${MEDPRIO_CONCURRENCY}
                  else
                    echo "There are no workers to set"
                  fi;;
            # Low prio workers can execute all, this workers should be busy most of the time
            "low_priority")
                  echo "Running $LOWPRIO_WORKER_NUM_PROCESSES low priority workers"
                  if [ $LOWPRIO_WORKER_NUM_PROCESSES -gt 0 ]; then
                    LOWPRIO_CONCURRENCY="--concurrency=${LOWPRIO_WORKER_NUM_PROCESSES}"
                    celery -A config worker -n mani_lowprio -Q highprio,medprio,lowprio,celery -l info ${LOWPRIO_CONCURRENCY}
                  else
                    echo "There are no workers to set"
                  fi;;
      esac;;
*)
  exec $*;;
esac
