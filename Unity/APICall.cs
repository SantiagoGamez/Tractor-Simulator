using UnityEngine;
using UnityEngine.Networking;
using System;
using System.Collections.Generic;
using System.Collections;

public class APICall : MonoBehaviour
{
    private string apiUrl = "http://127.0.0.1:5000/simulation"; // Tu endpoint de la API

    public GameObject harvester1; // Referencia al recolector 1 en Unity
    public GameObject harvester2; // Referencia al recolector 2 en Unity

    [Serializable]
    public class HarvestersData
    {
        public List<HarvesterData> harvester1;
        public List<HarvesterData> harvester2;
    }

    [Serializable]
    public class HarvesterData
    {
        public float X_COORDINATE;
        public float Z_COORDINATE;
    }

    void Start()
    {
        StartCoroutine(GetDataFromAPI());
    }

    IEnumerator GetDataFromAPI()
    {
        using (UnityWebRequest request = UnityWebRequest.Get(apiUrl))
        {
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                var jsonData = request.downloadHandler.text;
                Debug.Log("Received JSON Data: " + jsonData); // Log the received JSON data
                UpdateHarvesters(jsonData); // Update the harvesters with received data
            }
            else
            {
                Debug.LogError("Error: " + request.error);
            }
        }
    }

    void UpdateHarvesters(string jsonData)
    {
        Debug.Log("Received JSON Data: " + jsonData);

        try
        {
            HarvestersData data = JsonUtility.FromJson<HarvestersData>(jsonData);

            if (data != null)
            {
                MoveHarvester(data.harvester1, harvester1);
                MoveHarvester(data.harvester2, harvester2);
            }
            else
            {
                Debug.Log("No data available.");
            }
        }
        catch (Exception e)
        {
            Debug.LogError("Exception during deserialization or data handling: " + e);
        }
    }

    void MoveHarvester(List<HarvesterData> harvesterDataList, GameObject harvesterObject)
    {
        HarvesterController harvesterController = harvesterObject.GetComponent<HarvesterController>();

        if (harvesterController != null)
        {
            List<Vector3> harvesterCoordinates = GetHarvesterCoordinates(harvesterDataList);
            harvesterController.SetTargetPositions(harvesterCoordinates);
        }
        else
        {
            Debug.LogError("HarvesterController not found on " + harvesterObject.name);
        }
    }

    List<Vector3> GetHarvesterCoordinates(List<HarvesterData> harvesterDataList)
    {
        List<Vector3> harvesterCoordinates = new List<Vector3>();

        if (harvesterDataList != null && harvesterDataList.Count > 0)
        {
            foreach (var harvesterData in harvesterDataList)
            {
                float xCoordinate = harvesterData.X_COORDINATE;
                float zCoordinate = harvesterData.Z_COORDINATE;

                Vector3 newPosition = new Vector3(xCoordinate, 0f, zCoordinate);
                harvesterCoordinates.Add(newPosition);
            }
        }

        return harvesterCoordinates;
    }
}
