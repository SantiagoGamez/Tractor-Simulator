using UnityEngine;

public class SeguirObjeto : MonoBehaviour
{
    public Transform objetoASeguir;
    public Vector3 offset; // Esto te permite ajustar la posición relativa entre la cámara y el objeto

    void Update()
    {
        if (objetoASeguir != null)
        {
            // Obtén la posición del objeto a seguir y suma el offset
            Vector3 nuevaPosicion = objetoASeguir.position + offset;

            // Establece la posición de la cámara
            transform.position = nuevaPosicion;

            // Haz que la cámara mire hacia el objeto
            transform.LookAt(objetoASeguir);
        }
    }
}
