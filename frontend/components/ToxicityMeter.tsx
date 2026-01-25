interface Props {
    value: number;
}

export default function ToxicityMeter({value}: Props) {
    const color = 
    value <0.3 ? "bg-green-500":
    value <0.7 ? "bg-yellow-500":
    "bg-red-500"

    return (
        <div className="mt-2 w-full h-2 bg-gray-700 rounded">
            <div
            className={`${color} h-2 rounded transition-all`}
            style={{width: `${Math.min(value * 100, 100)}%`}}
            />
        </div>
    );
}