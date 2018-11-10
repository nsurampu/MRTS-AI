package com.example.asus.mrts;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;

public class TrainResultActivity extends AppCompatActivity {
    private String TAG = TrainResultActivity.class.getSimpleName();
    private RecyclerView trainList;
    private ProgressBar loadTrainDataProgressBar;
    private HashMap<String, String> trainData;
    private JSONObject trainJSON;
    private RecyclerViewAdpaterClass recyclerViewAdpaterClass;
    private Context context;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_train_result);
        trainList = findViewById(R.id.train_list);
        trainList.setAdapter(recyclerViewAdpaterClass);
        loadTrainDataProgressBar = findViewById(R.id.pb_load_train_data);
        trainData = new HashMap<>();
        context = this;
//        trainData.put("1", "3");
//        trainData.put("2", "4");
//        trainData.put("3", "5");
//        trainData.put("4", "6");
//        trainData.put("5", "7");
        Intent intent = getIntent();
        final String startStationName = intent.getStringExtra(QueryStation.SOURCE);
        final String destinationStationName = intent.getStringExtra(QueryStation.DESTINATION);
        String queryURL = QueryStation.URL + "route";
//        Log.d(TAG,queryURL);
        HashMap<String, String> params = new HashMap<>();
        params.put(QueryStation.SOURCE, startStationName);
        params.put(QueryStation.DESTINATION, destinationStationName);
        JSONObject paramsJSON = new JSONObject(params);

//        Log.d(TAG,""+paramsJSON);
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, queryURL, paramsJSON, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                Log.d(TAG, "RESPONSE: " + response);
                trainJSON = response;

                try {
//            {"0":[{"P601":"4:00"},{"P605":"5:20"}]}
                    Log.d(TAG, "trainJSON " + trainJSON);
                    JSONArray jsonArray = trainJSON.getJSONArray("0");
                    Log.d(TAG, "jsonArray " + jsonArray);
                    if (jsonArray == null) {
                        // TODO: print no trains exist
                        trainData.put("NO TRAINS EXIST", "NA");
                        Log.d(TAG, "null resp: " + trainData);
                        recyclerViewAdpaterClass = new RecyclerViewAdpaterClass(trainData);
                        trainList.setLayoutManager(new LinearLayoutManager(context));
//                        recyclerViewAdpaterClass.notifyDataSetChanged();
                        loadTrainDataProgressBar.setVisibility(View.GONE);
//                        trainList.setVisibility(View.VISIBLE);
                    } else {
                        for (int i = 0; i < jsonArray.length(); i++) {
                            JSONArray tempArray = jsonArray.getJSONArray(i);
                            Log.d(TAG, "temp" + tempArray);
                            String trainName = tempArray.getString(0);
                            String trainTime = tempArray.getString(1);
                            trainData.put(trainName, trainTime);
                            Log.d(TAG, trainName + " time: " + trainTime);
                        }
                        Log.d(TAG, "non null resp: " + trainData);
                        recyclerViewAdpaterClass = new RecyclerViewAdpaterClass(trainData);
                        trainList.setLayoutManager(new LinearLayoutManager(context));
//                        recyclerViewAdpaterClass.notifyDataSetChanged();
                        loadTrainDataProgressBar.setVisibility(View.GONE);
//                        trainList.setVisibility(View.VISIBLE);
                    }
                } catch (Exception e) {
                    Log.d(TAG, "ERROR " + e);
                    Log.d(TAG, "jsonarray null resp: " + trainData);
                    trainData.put("NO TRAINS EXIST", "NA");
                    recyclerViewAdpaterClass = new RecyclerViewAdpaterClass(trainData);
                    trainList.setLayoutManager(new LinearLayoutManager(context));
//                    recyclerViewAdpaterClass.notifyDataSetChanged();
                    loadTrainDataProgressBar.setVisibility(View.GONE);
//                    trainList.setVisibility(View.VISIBLE);
                }

            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.d(TAG, "request: " + error);
                trainData.put("NO TRAINS EXIST", "NA");
                loadTrainDataProgressBar.setVisibility(View.GONE);
                trainList.setVisibility(View.VISIBLE);
//                recyclerViewAdpaterClass.notifyDataSetChanged();
            }
        });
//        Log.d(TAG,jsonObjectRequest.getUrl());
//        Log.d(TAG,""+jsonObjectRequest.getBodyContentType());
//        Log.d(TAG,"request: "+ jsonObjectRequest);
        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(jsonObjectRequest);
    }

}
class RecyclerViewAdpaterClass extends RecyclerView.Adapter<ItemViewHolder> {
    private HashMap<String, String> trainNameAndTrainTime;
    private ArrayList<String> keySet;

    public RecyclerViewAdpaterClass(HashMap<String, String> trainNameAndTrainTime) {
        this.trainNameAndTrainTime = trainNameAndTrainTime;
        Log.d(TrainResultActivity.class.getSimpleName(),"ADAPTER: "+trainNameAndTrainTime);
        keySet = new ArrayList<>(trainNameAndTrainTime.keySet());
    }

    @Override
    public ItemViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        Context context = parent.getContext();
        int layoutIdForListItem = R.layout.train_item_layout;
        LayoutInflater inflater = LayoutInflater.from(context);
        boolean shouldAttachToParentImmediately = true;
        View v = inflater.inflate(layoutIdForListItem, parent, shouldAttachToParentImmediately);
        ItemViewHolder itemViewHolder = new ItemViewHolder(v);
        return itemViewHolder;
    }

    @Override
    public void onBindViewHolder(ItemViewHolder holder, int position) {
        Log.d(TrainResultActivity.class.getSimpleName(), "bind:" + position);
        holder.trainName.setText(keySet.get(position));
        holder.trainTime.setText(trainNameAndTrainTime.get(keySet.get(position)));
    }

    @Override
    public int getItemCount() {
        return keySet.size();
    }
}

class ItemViewHolder extends RecyclerView.ViewHolder {
    public TextView trainName;
    public TextView trainTime;
    public ItemViewHolder(View itemView) {
        super(itemView);
        trainName = itemView.findViewById(R.id.train_name);
        trainTime = itemView.findViewById(R.id.train_time);
    }
}
