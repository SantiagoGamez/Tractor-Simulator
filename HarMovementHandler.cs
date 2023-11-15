// Harvester movement handler
// JSON data format:
// { "coordinates": [ {"X_COORDINATE": 10.0, "Z_COORDINATE": 10.0 }, {"X_COORDINATE": 100.0, "Z_COORDINATE": 0.0 }, {"X_COORDINATE": 100.0, "Z_COORDINATE": 100.0 }, {"X_COORDINATE": 10.0, "Z_COORDINATE": 10.0 }, {"X_COORDINATE": 50.0, "Z_COORDINATE": 50.0 }, {"X_COORDINATE": 75.0, "Z_COORDINATE": 25.0 } ] }


using UnityEngine;
using System;
using System.Collections.Generic;

[Serializable]
public class PositionData
{
    public float X_COORDINATE;
    public float Z_COORDINATE;
}
[Serializable]
public class PositionDataList
{
    public List<PositionData> coordinates;
}


public class MovementHandler : MonoBehaviour
{
    public string jsonText;
    private string lastJsonText;
    private List<Vector3> targetPositions = new List<Vector3>();
    private int currentTargetIndex = 0;
    public float movementSpeed = 5.0f;

    void Start()
    {
        lastJsonText = jsonText;
        UpdateTargetPositions();
    }

    void Update()
    {
        if (jsonText != lastJsonText)
        {
            lastJsonText = jsonText;
            UpdateTargetPositions();
        }

        if (targetPositions.Count > 0)
        {
            // Calculate the direction of movement
            Vector3 direction = (targetPositions[currentTargetIndex] - transform.position).normalized;

            if (direction != Vector3.zero)
            {
                Quaternion toRotation = Quaternion.LookRotation(direction, Vector3.up);
                transform.rotation = Quaternion.RotateTowards(transform.rotation, toRotation, 5);
            }
            // Move the object towards the current target position
            transform.position = Vector3.MoveTowards(transform.position, targetPositions[currentTargetIndex], movementSpeed * Time.deltaTime);

            // Check if the object has reached the current target position
            if (Vector3.Distance(transform.position, targetPositions[currentTargetIndex]) < 0.1f)
            {
                // Move to the next target position
                currentTargetIndex = (currentTargetIndex + 1) % targetPositions.Count;
            }
        }
    }

        void UpdateTargetPosition()
    {
        PositionData data = JsonUtility.FromJson<PositionData>(jsonText);
        Vector3 targetPositionXZ = new Vector3(data.X_COORDINATE, 0, data.Z_COORDINATE);

        // Cast a ray downwards from the target XZ position
        RaycastHit hit;
        if (Physics.Raycast(targetPositionXZ + Vector3.up * 1000, Vector3.down, out hit))
        {
            // If the ray hits the terrain, set the target position to the hit point
            targetPosition = hit.point;
        }
        else
        {
            // If the ray does not hit the terrain, keep the current Y position
            targetPosition = new Vector3(data.X_COORDINATE, transform.position.y, data.Z_COORDINATE);
        }
    }


}