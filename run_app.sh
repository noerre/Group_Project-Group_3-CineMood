# It is not working correctly for now, don't run it

##Run backend
#if [ -d "backend" ]; then
#    if prompt_user "Do you want to start the backend server?"; then
#        echo "Starting the backend server..."
#        #cd backend || exit 1
#        source venv/Scripts/activate
#        python backend/app.py &
#        #cd ..
#    else
#        echo "Skipping backend server startup."
#    fi
#fi

## Run Frontend
#if [ -d "front-end" ]; then
#    if prompt_user "Do you want to start the frontend server?"; then
#        echo "Starting the frontend server..."
#        cd front-end || exit 1
#        npm start &
#        cd ..
#    else
#        echo "Skipping frontend server startup."
#    fi
#fi
#
#echo "Setup complete. If servers were started, access the application at http://localhost:3000."
