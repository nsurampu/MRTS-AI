package com.example.asus.mrts;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.Spinner;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.ArrayList;


public class QueryStation extends AppCompatActivity implements View.OnClickListener,AdapterView.OnItemSelectedListener{

    private String TAG = QueryStation.class.getSimpleName();
    public static String URL = "http://192.168.43.170:8080/client_query/";
    public static String SOURCE = "source";
    public static  String DESTINATION = "destination";
    private ProgressBar initialLoadBar;
    private Spinner sourceStation;
    private Spinner destinationStation;
    private JSONArray stationList;
    private Button searchStationButton;
    private String startStationName;
    private String destinationStationName;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_query_station);
        initialLoadBar = findViewById(R.id.progressbar_query_screen);
        sourceStation = findViewById(R.id.from_spinner);
        destinationStation = findViewById(R.id.to_spinner);
        searchStationButton = findViewById(R.id.search_button);
        searchStationButton.setOnClickListener(this);
        sourceStation.setOnItemSelectedListener(this);
        destinationStation.setOnItemSelectedListener(this);
    }

    @Override
    protected void onStart() {
        super.onStart();
        initialLoadBar.setVisibility(View.VISIBLE);
        String sendingURL = URL + "stations/";
        JsonArrayRequest jsonRequest = new JsonArrayRequest(Request.Method.GET, sendingURL, null, new Response.Listener<JSONArray>() {
            @Override
            public void onResponse(JSONArray response) {
                stationList = response;
                Log.d(TAG,"" + stationList);
                initialLoadBar.setVisibility(View.GONE);
                // TODO: populate a spinner with this list of Station names
                ArrayList<String> responseList = new ArrayList<>();
                for(int i = 0; i < stationList.length(); i++){
                    try {
                        responseList.add(stationList.getString(i));
                    }
                    catch (JSONException e){
                        Toast.makeText(QueryStation.this,"ERROR: ",Toast.LENGTH_SHORT).show();
                    }
                }
                Log.d(TAG,"responseList: " + responseList);
                ArrayAdapter adapterSource = new ArrayAdapter(QueryStation.this,android.R.layout.simple_spinner_dropdown_item,responseList);
                sourceStation.setAdapter(adapterSource);
                ArrayAdapter adapterDestination = new ArrayAdapter(QueryStation.this,android.R.layout.simple_spinner_dropdown_item,responseList);
                destinationStation.setAdapter(adapterDestination);
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(QueryStation.this, "Error loading data", Toast.LENGTH_SHORT).show();
                Log.d(TAG, "Error: " + error);
            }
        });
        RequestQueue requestQueue = Volley.newRequestQueue(this);

        requestQueue.add(jsonRequest);
    }


    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.search_button:
//                Toast.makeText(QueryStation.this,"HEHE",Toast.LENGTH_SHORT).show();
                Intent intent = new Intent(QueryStation.this,TrainResultActivity.class);
                intent.putExtra(SOURCE,startStationName);
                intent.putExtra(DESTINATION,destinationStationName);
                startActivity(intent);
            break;
        }
    }

    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
        switch (parent.getId()){
            case R.id.from_spinner:
                try {
                    startStationName = stationList.getString(position);
//                    Toast.makeText(QueryStation.this, "ERROR" + startStationName, Toast.LENGTH_SHORT).show();
                }
                catch (Exception e){
        //            Toast.makeText(QueryStation.this, "ERROR", Toast.LENGTH_SHORT).show();
                }
            break;

            case R.id.to_spinner:
                try {
                    destinationStationName= stationList.getString(position);
//                    Toast.makeText(QueryStation.this, "ERROR" + destinationStationName, Toast.LENGTH_SHORT).show();
                }
                catch (Exception e){
                    //            Toast.makeText(QueryStation.this, "ERROR", Toast.LENGTH_SHORT).show();
                }
            break;
        }

    }
    @Override
    public void onNothingSelected(AdapterView<?> parent) {
//        Toast.makeText(QueryStation.this,"NOT SELECTED",Toast.LENGTH_SHORT).show();
    }
}