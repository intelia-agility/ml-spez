const table_names = ["t1", "t2", "t3"];
table_names.forEach(table_name=>{
    publish(table_name, {
        type: "table",
        description: `${table_name} table is a dynamically generated table`
    })
    .query(ctx=>`SELECT * FROM ${ctx.ref("second_view")}`);
    assert(`assertion1 ${table_name}`).query(ctx=>`SELECT * FROM ${ctx.ref("second_view")} WHERE test>1`);
    operate(`operation for ${table_name}`,[`SELECT * FROM ${ctx.ref("second_view")}`]);
});
